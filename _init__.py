from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from .config import Config

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    jwt.init_app(app)
    
    Migrate(app, db)
    
    # Register Blueprints
    from .app.routes.auth import auth_bp
    from .app.routes.events import event_bp
    from .app.routes.tasks import task_bp
    from .app.routes.resources import resource_bp
    from .app.routes.expenses import expense_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(event_bp)
    app.register_blueprint(task_bp)
    app.register_blueprint(resource_bp)
    app.register_blueprint(expense_bp)

    return app
