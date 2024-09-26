# File: app/routes/admin.py
from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.models.ddns import DDNSProvider, DDNSConfig
from app.models.logs import AppLog
from app.models import db
from flask_login import login_required, current_user

admin = Blueprint('admin', __name__)

@admin.route('/admin/providers', methods=['GET'])
@login_required
def manage_providers():
    if current_user.role != 'admin':
        flash('Unauthorized access', 'error')
        return redirect(url_for('ddns.dashboard'))

    providers = DDNSProvider.query.all()
    return render_template('admin/providers.html', providers=providers)

@admin.route('/admin/add_provider', methods=['GET', 'POST'])
@login_required
def add_provider():
    if request.method == 'POST':
        name = request.form['name']
        update_url = request.form['update_url']
        required_fields = request.form.getlist('required_fields[]')
        required_fields = [{'field': field, 'label': field.capitalize()} for field in required_fields]
        DDNSProvider.add_provider(name, update_url, required_fields)
        AppLog.create(level='INFO', message=f"Added new DDNS Provider: {name}", module='admin')
        flash('Provider added successfully!', 'success')
        return redirect(url_for('admin.manage_providers'))
    
    return render_template('admin/add_provider.html')

@admin.route('/admin/edit_provider/<int:provider_id>', methods=['GET', 'POST'])
@login_required
def edit_provider(provider_id):
    provider = DDNSProvider.query.get_or_404(provider_id)
    if current_user.role != 'admin':
        flash('Unauthorized access', 'error')
        return redirect(url_for('ddns.dashboard'))

    if request.method == 'POST':
        provider.update_url = request.form['update_url']
        provider.required_fields = [{'field': field, 'label': field.capitalize()} for field in request.form.getlist('required_fields[]')]
        db.session.commit()
        AppLog.create(level='INFO', message=f"Updated DDNS Provider: {provider.name}", module='admin')
        flash('Provider updated successfully!', 'success')
        return redirect(url_for('admin.manage_providers'))

    return render_template('admin/edit_provider.html', provider=provider)

@admin.route('/admin/delete_provider/<int:provider_id>', methods=['POST'])
@login_required
def delete_provider(provider_id):
    provider = DDNSProvider.query.get_or_404(provider_id)
    db.session.delete(provider)
    db.session.commit()
    flash('Provider deleted successfully!', 'success')
    return redirect(url_for('admin.manage_providers'))
