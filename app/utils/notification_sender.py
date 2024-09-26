import smtplib
from email.mime.text import MIMEText
from app.models import db, GlobalNotificationSettings, NotificationLog

def send_email_notification(user, subject, body):
    settings = GlobalNotificationSettings.get_settings()
    
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = settings.smtp_from_email
    msg['To'] = user.email
    
    try:
        with smtplib.SMTP(settings.smtp_server, settings.smtp_port) as server:
            server.starttls()
            server.login(settings.smtp_username, settings.smtp_password)
            server.send_message(msg)
        
        log = NotificationLog(user_id=user.id, notification_type='email', message=subject, status='sent')
        db.session.add(log)
        db.session.commit()
        return True
    except Exception as e:
        log = NotificationLog(user_id=user.id, notification_type='email', message=f"Failed to send: {str(e)}", status='failed')
        db.session.add(log)
        db.session.commit()
        return False