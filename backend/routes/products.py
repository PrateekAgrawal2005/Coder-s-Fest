"""
Product Routes
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.database import db, Product, Review, Wishlist
from sqlalchemy import and_, or_

bp = Blueprint('products', __name__, url_prefix='/api/products')

@bp.route('', methods=['GET'])
def get_products():
    """Get all products with pagination and filtering"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        category = request.args.get('category')
        sort_by = request.args.get('sort_by', 'created_at')
        
        query = Product.query.filter_by(is_active=True)
        
        # Filter by category
        if category:
            query = query.filter_by(category=category)
        
        # Sort
        if sort_by == 'price_low':
            query = query.order_by(Product.price.asc())
        elif sort_by == 'price_high':
            query = query.order_by(Product.price.desc())
        elif sort_by == 'rating':
            query = query.order_by(Product.average_rating.desc())
        else:
            query = query.order_by(Product.created_at.desc())
        
        # Paginate
        paginated = query.paginate(page=page, per_page=per_page)
        
        return jsonify({
            'products': [p.to_dict() for p in paginated.items],
            'total': paginated.total,
            'pages': paginated.pages,
            'current_page': page
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/<product_id>', methods=['GET'])
def get_product(product_id):
    """Get single product details"""
    try:
        product = Product.query.get(product_id)
        
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        
        data = product.to_dict()
        data['reviews'] = [r.to_dict() for r in product.reviews.all()]
        
        return jsonify(data), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/search', methods=['POST'])
def search_products():
    """Search products with typo tolerance"""
    try:
        data = request.get_json()
        query_text = data.get('query', '').strip()
        
        if len(query_text) < 2:
            return jsonify({'error': 'Search query too short'}), 400
        
        # Search in product name and description
        products = Product.query.filter(
            and_(
                Product.is_active == True,
                or_(
                    Product.name.ilike(f'%{query_text}%'),
                    Product.description.ilike(f'%{query_text}%'),
                    Product.category.ilike(f'%{query_text}%')
                )
            )
        ).all()
        
        return jsonify({
            'results': [p.to_dict() for p in products],
            'count': len(products)
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/<product_id>/reviews', methods=['GET'])
def get_product_reviews(product_id):
    """Get reviews for a product"""
    try:
        product = Product.query.get(product_id)
        
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        
        reviews = Review.query.filter_by(product_id=product_id).all()
        
        return jsonify({
            'reviews': [r.to_dict() for r in reviews],
            'average_rating': product.average_rating,
            'total_reviews': product.total_reviews
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/<product_id>/reviews', methods=['POST'])
@jwt_required()
def add_review(product_id):
    """Add review for a product"""
    try:
        user_id = get_jwt_identity()
        product = Product.query.get(product_id)
        
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        
        data = request.get_json()
        rating = data.get('rating', 5)
        title = data.get('title', '')
        comment = data.get('comment', '')
        
        if not (1 <= rating <= 5):
            return jsonify({'error': 'Rating must be between 1 and 5'}), 400
        
        review = Review(
            product_id=product_id,
            user_id=user_id,
            rating=rating,
            title=title,
            comment=comment,
            verified_purchase=True
        )
        
        db.session.add(review)
        
        # Update product rating
        all_reviews = Review.query.filter_by(product_id=product_id).all()
        product.average_rating = sum(r.rating for r in all_reviews) / len(all_reviews)
        product.total_reviews = len(all_reviews)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Review added successfully',
            'review': review.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/<product_id>/wishlist', methods=['POST'])
@jwt_required()
def add_to_wishlist(product_id):
    """Add product to wishlist"""
    try:
        user_id = get_jwt_identity()
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
            'message': 'Added to wishlist',
            'item': wishlist_item.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
