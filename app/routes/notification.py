# File: app/routes/notification.py
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models.notification import GlobalNotificationSettings, UserNotificationSettings, NotificationLog
from app.models import db

notification = Blueprint('notification', __name__)

@notification.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if current_user.role != 'admin':
        flash('You do not have permission to access this page.', 'error')
        return redirect(url_for('ddns.dashboard'))

    global_settings = GlobalNotificationSettings.get_settings()

    if request.method == 'POST':
        global_settings.smtp_server = request.form['smtp_server']
        global_settings.smtp_port = int(request.form['smtp_port'])
        global_settings.smtp_username = request.form['smtp_username']
        global_settings.smtp_password = request.form['smtp_password']
        global_settings.smtp_use_tls = 'smtp_use_tls' in request.form
        global_settings.smtp_from_email = request.form['smtp_from_email']
        
        # Placeholder for SMS and Push notification settings
        global_settings.sms_api_key = request.form['sms_api_key']
        global_settings.push_api_key = request.form['push_api_key']
        
        db.session.commit()
        flash('Notification settings updated successfully.', 'success')
        return redirect(url_for('notification.settings'))

    return render_template('notification/settings.html', settings=global_settings)

@notification.route('/user_settings', methods=['GET', 'POST'])
@login_required
def user_settings():
    user_settings = UserNotificationSettings.query.filter_by(user_id=current_user.id).first()
    if not user_settings:
        user_settings = UserNotificationSettings(user_id=current_user.id)
        db.session.add(user_settings)
        db.session.commit()

    if request.method == 'POST':
        user_settings.email_enabled = 'email_enabled' in request.form
        user_settings.sms_enabled = 'sms_enabled' in request.form
        user_settings.push_enabled = 'push_enabled' in request.form
        user_settings.phone_number = request.form['phone_number']
        user_settings.device_token = request.form['device_token']
        
        db.session.commit()
        flash('Your notification preferences have been updated.', 'success')
        return redirect(url_for('notification.user_settings'))

    return render_template('notification/user_settings.html', settings=user_settings)

@notification.route('/logs')
@login_required
def logs():
    if current_user.role != 'admin':
        flash('You do not have permission to access this page.', 'error')
        return redirect(url_for('ddns.dashboard'))

    logs = NotificationLog.query.order_by(NotificationLog.timestamp.desc()).limit(100).all()
    return render_template('notification/logs.html', logs=logs)