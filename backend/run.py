"""
ElderConnect Application Entry Point
This file initializes and runs the Flask application.
"""
from app import create_app
import os

# Create Flask application instance
app = create_app()

if __name__ == '__main__':
    # Run the application
    # In production, use gunicorn instead
    app.run(
        host='0.0.0.0',
        port=int(os.getenv('PORT', 5000)),
        debug=os.getenv('FLASK_ENV') == 'development'
    )
