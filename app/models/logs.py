# File: app/models/logs.py
from app.models import db
from datetime import datetime
from sqlalchemy.ext.declarative import declared_attr

class AppLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    level = db.Column(db.String(20))  # 'INFO', 'WARNING', 'ERROR', etc.
    message = db.Column(db.Text)
    module = db.Column(db.String(50))  # The module or component that generated the log

    @classmethod
    def create(cls, level, message, module):
        log = cls(level=level, message=message, module=module)
        db.session.add(log)
        db.session.commit()
        return log

class DDNSUpdateLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ddns_config_id = db.Column(db.Integer, db.ForeignKey('ddns_config.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    success = db.Column(db.Boolean, nullable=False)
    message = db.Column(db.String(256))
    ip_address = db.Column(db.String(45))

    ddns_config = db.relationship('DDNSConfig', backref=db.backref('update_logs', lazy=True))
    
    @classmethod
    def create(cls, ddns_config_id, success, message, ip_address):
        log = cls(ddns_config_id=ddns_config_id, success=success, message=message, ip_address=ip_address)
        db.session.add(log)
        db.session.commit()
        return log
