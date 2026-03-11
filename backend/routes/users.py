"""
User Routes
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.database import db, User

bp = Blueprint('users', __name__, url_prefix='/api/users')

@bp.route('/loyalty-info', methods=['GET'])
@jwt_required()
def get_loyalty_info():
    """Get user loyalty program information"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        tiers = {
            'Bronze': {'min': 0, 'discount': 0},
            'Silver': {'min': 10000, 'discount': 5},
            'Gold': {'min': 30000, 'discount': 10},
            'Platinum': {'min': 50000, 'discount': 15}
        }
        
        next_tier_info = None
        tier_data = tiers[user.loyalty_tier]
        
        for tier_name, tier_info in tiers.items():
            if tier_info['min'] > user.total_spent:
                next_tier_info = {
                    'tier': tier_name,
                    'required_spent': tier_info['min'],
                    'remaining': tier_info['min'] - user.total_spent
                }
                break
        
        return jsonify({
            'current_tier': user.loyalty_tier,
            'loyalty_points': user.loyalty_points,
            'total_spent': user.total_spent,
            'discount_percentage': tier_data['discount'],
            'next_tier': next_tier_info,
            'benefits': [
                'Exclusive discounts',
                'Free shipping on orders',
                'Early access to sales',
                'Priority customer support',
                'Birthday rewards'
            ]
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/preferences', methods=['GET'])
@jwt_required()
def get_preferences():
    """Get user preferences"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'newsletter_subscribed': user.newsletter_subscribed,
            'preferred_language': user.preferred_language,
            'email_notifications': True,
            'sms_notifications': False
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/preferences', methods=['PUT'])
@jwt_required()
def update_preferences():
    """Update user preferences"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        
        if 'newsletter_subscribed' in data:
            user.newsletter_subscribed = data['newsletter_subscribed']
        
        if 'preferred_language' in data:
            user.preferred_language = data['preferred_language']
        
        db.session.commit()
        
        return jsonify({'message': 'Preferences updated'}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
