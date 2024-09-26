# file: app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    with app.app_context():
        from app.models import User, DDNSProvider, DDNSConfig, AppLog, DDNSUpdateLog
        from app.routes.auth import auth as auth_blueprint
        from app.routes.ddns import ddns as ddns_blueprint
        from app.routes.notification import notification as notification_blueprint
        from app.routes.logs import logs as logs_blueprint
        from app.routes.admin import admin as admin_blueprint
        from app.routes.scheduler import scheduler_bp

        app.register_blueprint(auth_blueprint)
        app.register_blueprint(ddns_blueprint)
        app.register_blueprint(notification_blueprint, url_prefix='/notification')
        # app.register_blueprint(logs_blueprint, url_prefix='/admin_logs')  # For Application Logs
        # app.register_blueprint(ddns_blueprint, url_prefix='/ddns_logs')   # For DDNS Logs
        app.register_blueprint(logs_blueprint, url_prefix='/logs')
        app.register_blueprint(admin_blueprint, url_prefix='/admin')
        app.register_blueprint(scheduler_bp, url_prefix='/health')

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app