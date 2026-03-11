"""
Payment Routes
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.database import db, Payment, Order
import hashlib
import hmac

bp = Blueprint('payments', __name__, url_prefix='/api/payments')

@bp.route('/initialize', methods=['POST'])
@jwt_required()
def initialize_payment():
    """Initialize payment gateway"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        order_id = data.get('order_id')
        method = data.get('method')  # card, upi, wallet, cod
        
        order = Order.query.get(order_id)
        if not order or order.user_id != user_id:
            return jsonify({'error': 'Order not found'}), 404
        
        # Mock payment gateway initialization
        payment_options = {
            'card': {
                'gateway': 'Stripe',
                'public_key': 'pk_test_mock_key',
                'amount': order.total
            },
            'upi': {
                'gateway': 'Razorpay',
                'upi_id': 'merchant@upi',
                'amount': order.total
            },
            'wallet': {
                'gateway': 'Wallet Service',
                'balance': 5000,
                'required': order.total
            },
            'cod': {
                'gateway': 'Cash on Delivery',
                'amount': order.total
            }
        }
        
        return jsonify({
            'payment_session': payment_options.get(method, {}),
            'order_id': order_id,
            'amount': order.total
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/process', methods=['POST'])
@jwt_required()
def process_payment():
    """Process payment"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        order_id = data.get('order_id')
        method = data.get('method')
        transaction_id = data.get('transaction_id', f'TXN_{order_id}')
        
        order = Order.query.get(order_id)
        if not order or order.user_id != user_id:
            return jsonify({'error': 'Order not found'}), 404
        
        # Create payment record
        payment = Payment(
            order_id=order_id,
            method=method,
            amount=order.total,
            status='completed',
            transaction_id=transaction_id,
            reference_id=f'REF_{order_id}'
        )
        
        order.payment_status = 'completed'
        order.status = 'processing'
        
        db.session.add(payment)
        db.session.commit()
        
        return jsonify({
            'message': 'Payment processed successfully',
            'payment': {
                'transaction_id': transaction_id,
                'amount': payment.amount,
                'status': payment.status,
                'method': payment.method
            }
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/<order_id>/receipt', methods=['GET'])
@jwt_required()
def get_payment_receipt(order_id):
    """Get payment receipt"""
    try:
        user_id = get_jwt_identity()
        order = Order.query.get(order_id)
        
        if not order or order.user_id != user_id:
            return jsonify({'error': 'Order not found'}), 404
        
        payment = Payment.query.filter_by(order_id=order_id).first()
        
        if not payment:
            return jsonify({'error': 'Payment not found'}), 404
        
        return jsonify({
            'receipt_number': f'RCP-{order_id}',
            'order_number': order.order_number,
            'date': order.created_at.isoformat(),
            'amount': payment.amount,
            'method': payment.method,
            'transaction_id': payment.transaction_id,
            'status': payment.status
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
