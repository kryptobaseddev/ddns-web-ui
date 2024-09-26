# File: app/models/ddns.py
from app.models import db
from datetime import datetime

class DDNSProvider(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)  # Predefined, non-editable
    update_url = db.Column(db.String(256), nullable=False)
    required_fields = db.Column(db.JSON, nullable=False)  # Example: [{"field": "domain", "label": "Domain"}, {"field": "token", "label": "Token"}]
    
    @classmethod
    def add_provider(cls, name, update_url, required_fields):
        # Only allow adding of predefined providers via the admin or a script
        provider = cls(name=name, update_url=update_url, required_fields=required_fields)
        db.session.add(provider)
        db.session.commit()
        return provider

class DDNSConfig(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Re-add user_id
    provider_id = db.Column(db.Integer, db.ForeignKey('ddns_provider.id'), nullable=False)
    config_values = db.Column(db.JSON, nullable=False)
    update_interval = db.Column(db.Integer, default=5)
    last_update_attempt = db.Column(db.DateTime)
    last_successful_update = db.Column(db.DateTime)
    current_ip = db.Column(db.String(45))  # To store the current external IP

    user = db.relationship('User', backref=db.backref('ddns_configs', lazy=True))
    provider = db.relationship('DDNSProvider', backref=db.backref('configs', lazy=True))

    def update_config(self, new_config_values):
        required_fields = self.provider.required_fields
        missing_fields = [field['field'] for field in required_fields if field['field'] not in new_config_values]
        if missing_fields:
            raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")
        
        self.config_values = new_config_values
        db.session.commit()

