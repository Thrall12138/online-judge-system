"""
Flask application setup for Online Judge System
Handles database initialization and API route configuration
"""

from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from datetime import datetime

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name='development'):
    """
    Application factory for creating Flask app instances
    
    Args:
        config_name: Configuration environment (development, testing, production)
    
    Returns:
        Flask application instance
    """
    app = Flask(__name__)
    
    # Configuration based on environment
    if config_name == 'development':
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
            'DEV_DATABASE_URL',
            'sqlite:///online_judge.db'
        )
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['DEBUG'] = True
    elif config_name == 'testing':
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['TESTING'] = True
    elif config_name == 'production':
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['DEBUG'] = False
    
    # Application configuration
    app.config['JSON_SORT_KEYS'] = False
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max request size
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)
    
    # Register error handlers
    register_error_handlers(app)
    
    # Register blueprints and API routes
    register_blueprints(app)
    
    # Register CLI commands
    register_cli_commands(app)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app


def register_blueprints(app):
    """
    Register API blueprints
    
    Args:
        app: Flask application instance
    """
    # Health check endpoint
    @app.route('/api/health', methods=['GET'])
    def health_check():
        """Health check endpoint"""
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat(),
            'service': 'online-judge-system'
        }), 200
    
    # API info endpoint
    @app.route('/api/info', methods=['GET'])
    def api_info():
        """API information endpoint"""
        return jsonify({
            'name': 'Online Judge System API',
            'version': '1.0.0',
            'description': 'Backend API for competitive programming online judge',
            'endpoints': {
                'health': '/api/health',
                'info': '/api/info'
            }
        }), 200
    
    # Import and register blueprints (these will be created as needed)
    try:
        from routes.problems import problems_bp
        app.register_blueprint(problems_bp, url_prefix='/api/problems')
    except ImportError:
        app.logger.info('Problems blueprint not yet available')
    
    try:
        from routes.submissions import submissions_bp
        app.register_blueprint(submissions_bp, url_prefix='/api/submissions')
    except ImportError:
        app.logger.info('Submissions blueprint not yet available')
    
    try:
        from routes.users import users_bp
        app.register_blueprint(users_bp, url_prefix='/api/users')
    except ImportError:
        app.logger.info('Users blueprint not yet available')
    
    try:
        from routes.contests import contests_bp
        app.register_blueprint(contests_bp, url_prefix='/api/contests')
    except ImportError:
        app.logger.info('Contests blueprint not yet available')


def register_error_handlers(app):
    """
    Register error handlers for common HTTP errors
    
    Args:
        app: Flask application instance
    """
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 Not Found errors"""
        return jsonify({
            'error': 'Not Found',
            'message': 'The requested resource was not found',
            'status': 404
        }), 404
    
    @app.errorhandler(400)
    def bad_request(error):
        """Handle 400 Bad Request errors"""
        return jsonify({
            'error': 'Bad Request',
            'message': 'The request is invalid or malformed',
            'status': 400
        }), 400
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 Internal Server errors"""
        db.session.rollback()
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'An unexpected error occurred',
            'status': 500
        }), 500
    
    @app.errorhandler(403)
    def forbidden(error):
        """Handle 403 Forbidden errors"""
        return jsonify({
            'error': 'Forbidden',
            'message': 'You do not have permission to access this resource',
            'status': 403
        }), 403
    
    @app.errorhandler(401)
    def unauthorized(error):
        """Handle 401 Unauthorized errors"""
        return jsonify({
            'error': 'Unauthorized',
            'message': 'Authentication is required to access this resource',
            'status': 401
        }), 401


def register_cli_commands(app):
    """
    Register CLI commands for database management
    
    Args:
        app: Flask application instance
    """
    @app.cli.command()
    def init_db():
        """Initialize the database"""
        db.create_all()
        print('Database initialized successfully')
    
    @app.cli.command()
    def drop_db():
        """Drop all database tables"""
        if os.environ.get('FLASK_ENV') != 'production':
            db.drop_all()
            print('Database dropped successfully')
        else:
            print('Cannot drop database in production environment')
    
    @app.cli.command()
    def seed_db():
        """Seed database with initial data"""
        print('Seeding database...')
        # Database seeding logic will be implemented here
        print('Database seeded successfully')


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
