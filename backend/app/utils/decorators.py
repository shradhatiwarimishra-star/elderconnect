"""
Custom decorators for route protection and authorization
"""
from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from app.models.user import User


def role_required(*allowed_roles):
    """
    Decorator to require specific user roles
    Usage: @role_required('elder', 'caregiver')
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            # Verify JWT token
            verify_jwt_in_request()
            
            # Get current user
            current_user_id = get_jwt_identity()
            user = User.query.get(current_user_id)
            
            if not user:
                return jsonify({'error': 'User not found'}), 404
            
            if not user.is_active:
                return jsonify({'error': 'Account is inactive'}), 403
            
            # Check if user has required role
            if user.role not in allowed_roles:
                return jsonify({'error': 'Insufficient permissions'}), 403
            
            return fn(*args, **kwargs)
        
        return wrapper
    return decorator


def kyc_verified_required(fn):
    """
    Decorator to require KYC verification
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        if user.kyc_status != 'verified':
            return jsonify({'error': 'KYC verification required'}), 403
        
        return fn(*args, **kwargs)
    
    return wrapper
