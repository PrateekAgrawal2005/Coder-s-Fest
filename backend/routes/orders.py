"""
Order Routes
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.database import db, Order, OrderItem, Product, User
from datetime import datetime
import uuid

bp = Blueprint('orders', __name__, url_prefix='/api/orders')

@bp.route('', methods=['GET'])
@jwt_required()
def get_orders():
    """Get user orders"""
    try:
        user_id = get_jwt_identity()
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        orders = Order.query.filter_by(user_id=user_id).order_by(Order.created_at.desc()).paginate(page=page, per_page=per_page)
        
        return jsonify({
            'orders': [o.to_dict() for o in orders.items],
            'total': orders.total,
            'pages': orders.pages,
            'current_page': page
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/<order_id>', methods=['GET'])
@jwt_required()
def get_order(order_id):
    """Get order details"""
    try:
        user_id = get_jwt_identity()
        order = Order.query.get(order_id)
        
        if not order:
            return jsonify({'error': 'Order not found'}), 404
        
        if order.user_id != user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        return jsonify(order.to_dict()), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('', methods=['POST'])
@jwt_required()
def create_order():
    """Create new order"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        
        items = data.get('items', [])
        shipping_address = data.get('shipping_address')
        
        if not items:
            return jsonify({'error': 'No items in order'}), 400
        
        if not shipping_address:
            return jsonify({'error': 'Shipping address required'}), 400
        
        # Calculate totals
        subtotal = 0
        order_items = []
        
        for item in items:
            product = Product.query.get(item['product_id'])
            
            if not product:
                return jsonify({'error': f'Product {item["product_id"]} not found'}), 404
            
            if product.stock < item['quantity']:
                return jsonify({'error': f'Insufficient stock for {product.name}'}), 400
            
            item_total = product.price * item['quantity']
            subtotal += item_total
            
            order_item = OrderItem(
                product_id=product.id,
                quantity=item['quantity'],
                price=product.price
            )
            order_items.append(order_item)
            
            # Reduce stock
            product.stock -= item['quantity']
        
        # Calculate tax and shipping
        tax = subtotal * 0.18  # 18% GST
        shipping = 99 if subtotal < 500 else 0  # Free shipping above 500
        discount = data.get('discount', 0)
        total = subtotal + tax + shipping - discount
        
        # Create order
        order = Order(
            order_number=f"ORD-{uuid.uuid4().hex[:8].upper()}",
            user_id=user_id,
            subtotal=subtotal,
            tax=tax,
            shipping=shipping,
            discount=discount,
            total=total,
            shipping_address=shipping_address,
            status='confirmed',
            payment_status='pending'
        )
        
        db.session.add(order)
        db.session.flush()  # Flush to get order ID
        
        # Add items to order
        for order_item in order_items:
            order_item.order_id = order.id
            db.session.add(order_item)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Order created successfully',
            'order': order.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/<order_id>/cancel', methods=['POST'])
@jwt_required()
def cancel_order(order_id):
    """Cancel an order"""
    try:
        user_id = get_jwt_identity()
        order = Order.query.get(order_id)
        
        if not order:
            return jsonify({'error': 'Order not found'}), 404
        
        if order.user_id != user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        if order.status in ['shipped', 'delivered', 'cancelled']:
            return jsonify({'error': f'Cannot cancel order with status: {order.status}'}), 400
        
        order.status = 'cancelled'
        order.payment_status = 'refunded'
        
        # Restore stock
        for item in order.items:
            item.product.stock += item.quantity
        
        db.session.commit()
        
        return jsonify({
            'message': 'Order cancelled successfully',
            'order': order.to_dict()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/<order_id>/track', methods=['GET'])
@jwt_required()
def track_order(order_id):
    """Track order status"""
    try:
        user_id = get_jwt_identity()
        order = Order.query.get(order_id)
        
        if not order:
            return jsonify({'error': 'Order not found'}), 404
        
        if order.user_id != user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        timeline = [
            {'status': 'confirmed', 'timestamp': order.created_at.isoformat(), 'message': 'Order Confirmed'},
            {'status': 'processing', 'timestamp': (order.created_at).isoformat() if order.status != 'pending' else None, 'message': 'Processing'},
            {'status': 'shipped', 'timestamp': order.shipped_at.isoformat() if order.shipped_at else None, 'message': 'Shipped'},
            {'status': 'delivered', 'timestamp': order.delivered_at.isoformat() if order.delivered_at else None, 'message': 'Delivered'}
        ]
        
        return jsonify({
            'order_id': order_id,
            'current_status': order.status,
            'timeline': [t for t in timeline if t['timestamp']],
            'estimated_delivery': 'In 3-5 business days'
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
