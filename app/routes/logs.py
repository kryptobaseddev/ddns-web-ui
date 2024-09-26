# File: app/routes/logs.py
from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from app.models.logs import AppLog, DDNSUpdateLog

logs = Blueprint('logs', __name__)

# Application Logs Route
@logs.route('/application_logs')
@login_required
def view_application_logs():
    if current_user.role != 'admin':
        flash('You do not have permission to access this page.', 'error')
        return redirect(url_for('ddns.dashboard'))

    app_logs = AppLog.query.order_by(AppLog.timestamp.desc()).limit(100).all()
    return render_template('admin/logs.html', logs=app_logs)

# DDNS Logs Route
@logs.route('/ddns_logs')
@login_required
def view_ddns_logs():
    # Show all DDNS update logs, regardless of user
    ddns_logs = DDNSUpdateLog.query.order_by(DDNSUpdateLog.timestamp.desc()).limit(100).all()
    return render_template('ddns/logs.html', logs=ddns_logs)

