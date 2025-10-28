"""
File upload utilities
"""
import os
import uuid
from werkzeug.utils import secure_filename
from flask import current_app


def save_uploaded_file(file, folder='general'):
    """
    Save uploaded file to the uploads directory
    
    Args:
        file: FileStorage object from request.files
        folder: Subfolder within uploads directory
    
    Returns:
        Relative path to saved file or None if error
    """
    if not file:
        return None
    
    # Generate unique filename
    filename = secure_filename(file.filename)
    unique_filename = f"{uuid.uuid4().hex}_{filename}"
    
    # Create full path
    upload_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], folder)
    os.makedirs(upload_folder, exist_ok=True)
    
    file_path = os.path.join(upload_folder, unique_filename)
    
    # Save file
    file.save(file_path)
    
    # Return relative path
    return os.path.join(folder, unique_filename)


def delete_file(file_path):
    """
    Delete a file from uploads directory
    
    Args:
        file_path: Relative path to file
    
    Returns:
        True if successful, False otherwise
    """
    try:
        full_path = os.path.join(current_app.config['UPLOAD_FOLDER'], file_path)
        if os.path.exists(full_path):
            os.remove(full_path)
            return True
        return False
    except Exception as e:
        current_app.logger.error(f"Error deleting file: {str(e)}")
        return False


def get_file_url(file_path):
    """
    Generate URL for uploaded file
    
    Args:
        file_path: Relative path to file
    
    Returns:
        Full URL to access file
    """
    if not file_path:
        return None
    
    # In production, this would be your CDN or file server URL
    return f"/uploads/{file_path}"
