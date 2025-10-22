"""
Validation utilities for request data
"""
import re
from email_validator import validate_email, EmailNotValidError


def validate_email_format(email):
    """
    Validate email format
    Returns: (is_valid, error_message)
    """
    try:
        validate_email(email)
        return True, None
    except EmailNotValidError as e:
        return False, str(e)


def validate_password_strength(password):
    """
    Validate password strength
    Requirements: At least 8 characters, 1 uppercase, 1 lowercase, 1 number
    Returns: (is_valid, error_message)
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    
    if not re.search(r'\d', password):
        return False, "Password must contain at least one number"
    
    return True, None


def validate_phone_number(phone):
    """
    Validate phone number format (US format)
    Returns: (is_valid, error_message)
    """
    if not phone:
        return True, None  # Phone is optional
    
    # Remove common formatting characters
    cleaned = re.sub(r'[\s\-\(\)\.]', '', phone)
    
    # Check if it's a valid US phone number (10 digits)
    if not re.match(r'^\+?1?\d{10}$', cleaned):
        return False, "Invalid phone number format. Use 10-digit US format."
    
    return True, None


def validate_rating(rating):
    """
    Validate rating value (1-5)
    Returns: (is_valid, error_message)
    """
    try:
        rating_int = int(rating)
        if 1 <= rating_int <= 5:
            return True, None
        return False, "Rating must be between 1 and 5"
    except (ValueError, TypeError):
        return False, "Rating must be a valid integer"


def allowed_file(filename, allowed_extensions):
    """
    Check if file extension is allowed
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions
