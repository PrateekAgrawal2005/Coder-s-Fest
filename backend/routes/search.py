"""
Search Routes
"""

from flask import Blueprint, request, jsonify
from models.database import db, Product
from sqlalchemy import or_

bp = Blueprint('search', __name__, url_prefix='/api/search')

@bp.route('', methods=['GET', 'POST'])
def search():
    """Search products"""
    try:
        if request.method == 'POST':
            data = request.get_json()
            query = data.get('query', '').strip()
        else:
            query = request.args.get('q', '').strip()
        
        if len(query) < 2:
            return jsonify({'error': 'Search query too short'}), 400
        
        # Search in multiple fields
        results = Product.query.filter(
            Product.is_active == True,
            or_(
                Product.name.ilike(f'%{query}%'),
                Product.description.ilike(f'%{query}%'),
                Product.category.ilike(f'%{query}%')
            )
        ).limit(20).all()
        
        return jsonify({
            'query': query,
            'results': [p.to_dict() for p in results],
            'count': len(results)
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/suggestions', methods=['GET'])
def get_suggestions():
    """Get search suggestions"""
    try:
        query = request.args.get('q', '').strip()
        
        if len(query) < 1:
            return jsonify({'suggestions': []}), 200
        
        # Get matching categories
        categories = db.session.query(Product.category).filter(
            Product.category.ilike(f'%{query}%'),
            Product.is_active == True
        ).distinct().limit(5).all()
        
        # Get matching products
        products = Product.query.filter(
            Product.name.ilike(f'%{query}%'),
            Product.is_active == True
        ).limit(5).all()
        
        suggestions = [
            {'type': 'category', 'text': cat[0]} for cat in categories
        ] + [
            {'type': 'product', 'text': p.name} for p in products
        ]
        
        return jsonify({'suggestions': suggestions}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
