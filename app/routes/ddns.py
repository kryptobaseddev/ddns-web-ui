# File: app/routes/ddns.py
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app.models.ddns import DDNSConfig, DDNSProvider
from app.models.logs import DDNSUpdateLog, AppLog
from app.models import db
from app.utils.ddns_updater import update_ddns, get_current_ip
from datetime import datetime

ddns = Blueprint('ddns', __name__)

@ddns.route('/')
@login_required
def dashboard():
    # Get the current user's configurations
    configs = DDNSConfig.query.all()
    current_ip = get_current_ip()

    # Convert configs into a JSON-serializable format
    config_data = []
    for config in configs:
        config_data.append({
            'id': config.id,
            'provider': config.provider.name,
            'domain': config.config_values.get('domain', ''),
            'last_update_attempt': config.last_update_attempt.isoformat() if config.last_update_attempt else None,
            'last_successful_update': config.last_successful_update.isoformat() if config.last_successful_update else None,
            'current_ip': config.current_ip,
            'update_interval': config.update_interval
        })

    return render_template('ddns/dashboard.html', configs=config_data, current_ip=current_ip)

@ddns.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    # Only Admins should access the settings
    if current_user.role != 'admin':
        flash('You do not have permission to access DDNS Settings.', 'error')
        return redirect(url_for('ddns.dashboard'))

    if request.method == 'POST':
        # Handle configuration update logic here...
        # Only admins can modify configurations
        if request.method == 'POST':
            if 'delete' in request.form:
                # Delete existing configuration
                config_id = request.form['delete']
                config = DDNSConfig.query.get(config_id)
                if config and current_user.role == 'admin':  # Only allow admins to delete
                    db.session.delete(config)
                    db.session.commit()
                    flash(f'DDNS configuration for {config.provider.name} deleted successfully', 'success')
                else:
                    flash('You do not have permission to delete this configuration', 'error')
            elif 'config_id' in request.form:
                # Update existing configuration
                config_id = request.form['config_id']
                config = DDNSConfig.query.get(config_id)
                if config and current_user.role == 'admin':  # Only allow admins to update
                    config.update_config({
                        field['field']: request.form[field['field']] for field in config.provider.required_fields
                    })
                    config.update_interval = int(request.form['update_interval'])
                    db.session.commit()
                    AppLog.create(level='INFO', message=f"DDNS configuration updated for {config.provider.name}", module='ddns')
                    flash('Configuration updated successfully', 'success')
            else:
                # Add new configuration
                provider_id = request.form['provider']
                new_config = DDNSConfig(
                    user_id=current_user.id,  # Add user_id when creating a new config
                    provider_id=provider_id,
                    config_values={
                        field['field']: request.form[field['field']] for field in DDNSProvider.query.get(provider_id).required_fields
                    },
                    update_interval=int(request.form['update_interval'])
                )
                db.session.add(new_config)
                db.session.commit()
                AppLog.create(level='INFO', message=f"Added new DDNS configuration for provider {new_config.provider.name}", module='ddns')
                flash('New configuration added successfully', 'success')
        pass
    
    # Show all configurations and providers for Admins to modify
    configs = DDNSConfig.query.all()
    providers = DDNSProvider.query.all()
    return render_template('ddns/settings.html', configs=configs, providers=providers)

@ddns.route('/update/<int:config_id>', methods=['POST'])
@login_required
def update(config_id):
    config = DDNSConfig.query.get(config_id)
    if config and config.user_id == current_user.id:
        success, message, ip_address = update_ddns(config)
        log = DDNSUpdateLog(ddns_config_id=config.id, success=success, message=message, ip_address=ip_address)
        db.session.add(log)
        db.session.commit()
        if success:
            flash('DDNS updated successfully', 'success')
        else:
            flash(f'DDNS update failed: {message}', 'error')
    else:
        flash('Invalid configuration', 'error')
    return redirect(url_for('ddns.dashboard'))

@ddns.route('/manual_update/<int:config_id>', methods=['POST'])
@login_required
def manual_update(config_id):
    config = DDNSConfig.query.get_or_404(config_id)

    # Perform the update
    success, message, ip = update_ddns(config)

    # Log the DDNS update with the current user's information (for auditing)
    ddns_log = DDNSUpdateLog(
        ddns_config_id=config.id,
        success=success,
        message=f"{message} (Triggered by user: {current_user.username})",  # Add user info to the log
        ip_address=ip if success else 'N/A'
    )

    db.session.add(ddns_log)
    db.session.commit()

    # Update the configuration last attempt details
    if success:
        config.last_successful_update = datetime.utcnow()
        config.current_ip = ip
    config.last_update_attempt = datetime.utcnow()
    db.session.commit()

    flash(message, 'success' if success else 'error')
    return redirect(url_for('ddns.dashboard'))


@ddns.route('/backup')
@login_required
def backup():
    # Implement backup functionality
    return render_template('ddns/backup.html')

@ddns.route('/get_provider_fields', methods=['GET'])
@login_required
def get_provider_fields():
    provider_id = request.args.get('provider_id')
    provider = DDNSProvider.query.get(provider_id)
    if not provider:
        return jsonify({"error": "Provider not found"}), 404

    return jsonify({"required_fields": provider.required_fields})
