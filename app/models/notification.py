# File: app/models/notification.py
from app.models import db
from datetime import datetime

class GlobalNotificationSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    # Email (SMTP) settings
    smtp_server = db.Column(db.String(128))
    smtp_port = db.Column(db.Integer, default=587)
    smtp_username = db.Column(db.String(128))
    smtp_password = db.Column(db.String(128))
    smtp_from_email = db.Column(db.String(128))
    
    # SMS settings (placeholder)
    sms_api_key = db.Column(db.String(128))
    sms_api_secret = db.Column(db.String(128))
    
    # Push notification settings (placeholder)
    push_api_key = db.Column(db.String(128))

    @classmethod
    def get_settings(cls):
        settings = cls.query.first()
        if not settings:
            settings = cls()
            db.session.add(settings)
            db.session.commit()
        return settings

class UserNotificationSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    email_enabled = db.Column(db.Boolean, default=True)
    sms_enabled = db.Column(db.Boolean, default=False)
    push_enabled = db.Column(db.Boolean, default=False)
    
    phone_number = db.Column(db.String(20))  # For SMS notifications
    device_token = db.Column(db.String(256))  # For push notifications

class NotificationLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    notification_type = db.Column(db.String(20))  # 'email', 'sms', or 'push'
    message = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20))  # 'sent', 'failed', etc.

    user = db.relationship('User', backref=db.backref('notification_logs', lazy=True))
    