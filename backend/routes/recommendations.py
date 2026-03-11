"""
Recommendations Routes
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.database import db, Product, Order, OrderItem

bp = Blueprint('recommendations', __name__, url_prefix='/api/recommendations')

@bp.route('/personalized', methods=['GET'])
@jwt_required()
def get_personalized_recommendations():
    """Get personalized product recommendations"""
    try:
        user_id = get_jwt_identity()
        
        # Get user's purchase history
        user_orders = Order.query.filter_by(user_id=user_id).all()
        user_categories = set()
        
        for order in user_orders:
            for item in order.items:
                user_categories.add(item.product.category)
        
        # Get top-rated products from user's categories
        recommendations = []
        
        if user_categories:
            for category in list(user_categories)[:3]:
                category_products = Product.query.filter(
                    Product.category == category,
                    Product.is_active == True
                ).order_by(Product.average_rating.desc()).limit(2).all()
                recommendations.extend(category_products)
        
        # If no purchase history, get trending products
        if not recommendations:
            recommendations = Product.query.filter_by(is_active=True)\
                .order_by(Product.total_reviews.desc()).limit(8).all()
        
        return jsonify({
            'recommendations': [p.to_dict() for p in recommendations[:8]],
            'reason': 'Based on your interests' if user_categories else 'Trending now'
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/trending', methods=['GET'])
def get_trending_products():
    """Get trending products"""
    try:
        trending = Product.query.filter_by(is_active=True)\
            .order_by(Product.total_reviews.desc())\
            .limit(10).all()
        
        return jsonify({
            'products': [p.to_dict() for p in trending]
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/crosssell/<product_id>', methods=['GET'])
def get_crosssell(product_id):
    """Get cross-sell recommendations for a product"""
    try:
        product = Product.query.get(product_id)
        
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        
        # Get products from different categories but similar price range
        similar_price = Product.query.filter(
            Product.category != product.category,
            Product.price >= product.price * 0.8,
            Product.price <= product.price * 1.2,
            Product.is_active == True
        ).limit(4).all()
        
        return jsonify({
            'crosssell_products': [p.to_dict() for p in similar_price]
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
