"""
Wishlist Routes
Handle user wishlist management: view, add, remove items
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.database import db, Wishlist, Product
from sqlalchemy import desc

bp = Blueprint('wishlist', __name__, url_prefix='/api/wishlist')


@bp.route('', methods=['POST'])
@jwt_required()
def add_to_wishlist():
    """Add item to wishlist"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        product_id = data.get('product_id')
        if not product_id:
            return jsonify({'error': 'Product ID required'}), 400
        
        # Check if product exists
        product = Product.query.get(product_id)
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        
        # Check if already in wishlist
        existing = Wishlist.query.filter_by(user_id=user_id, product_id=product_id).first()
        if existing:
            return jsonify({'error': 'Product already in wishlist'}), 409
        
        wishlist_item = Wishlist(user_id=user_id, product_id=product_id)
        db.session.add(wishlist_item)
        db.session.commit()
        
        return jsonify({
            'message': 'Item added to wishlist',
            'item': wishlist_item.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('', methods=['GET'])
@jwt_required()
def get_wishlist():
    """Get all items in user's wishlist"""
    try:
        user_id = get_jwt_identity()
        
        # Get all wishlist items for the user, ordered by most recent
        wishlist_items = Wishlist.query.filter_by(user_id=user_id).order_by(desc(Wishlist.created_at)).all()
        
        return jsonify({
            'count': len(wishlist_items),
            'items': [item.to_dict() for item in wishlist_items]
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/<wishlist_id>', methods=['DELETE'])
@jwt_required()
def remove_from_wishlist(wishlist_id):
    """Remove item from wishlist"""
    try:
        user_id = get_jwt_identity()
        
        # Find the wishlist item
        wishlist_item = Wishlist.query.get(wishlist_id)
        
        if not wishlist_item:
            return jsonify({'error': 'Wishlist item not found'}), 404
        
        # Verify ownership - user can only delete their own wishlist items
        if wishlist_item.user_id != user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        db.session.delete(wishlist_item)
        db.session.commit()
        
        return jsonify({
            'message': 'Item removed from wishlist',
            'wishlist_id': wishlist_id
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/product/<product_id>', methods=['DELETE'])
@jwt_required()
def remove_product_from_wishlist(product_id):
    """Remove product from wishlist by product ID"""
    try:
        user_id = get_jwt_identity()
        
        # Find the wishlist item by user and product
        wishlist_item = Wishlist.query.filter_by(user_id=user_id, product_id=product_id).first()
        
        if not wishlist_item:
            return jsonify({'error': 'Item not in wishlist'}), 404
        
        db.session.delete(wishlist_item)
        db.session.commit()
        
        return jsonify({
            'message': 'Product removed from wishlist',
            'product_id': product_id
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/clear', methods=['DELETE'])
@jwt_required()
def clear_wishlist():
    """Clear entire wishlist"""
    try:
        user_id = get_jwt_identity()
        
        # Delete all wishlist items for the user
        count = Wishlist.query.filter_by(user_id=user_id).delete()
        db.session.commit()
        
        return jsonify({
            'message': 'Wishlist cleared',
            'items_removed': count
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/check/<product_id>', methods=['GET'])
@jwt_required()
def check_if_in_wishlist(product_id):
    """Check if product is in user's wishlist"""
    try:
        user_id = get_jwt_identity()
        
        wishlist_item = Wishlist.query.filter_by(user_id=user_id, product_id=product_id).first()
        
        return jsonify({
            'in_wishlist': wishlist_item is not None,
            'wishlist_id': wishlist_item.id if wishlist_item else None
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
