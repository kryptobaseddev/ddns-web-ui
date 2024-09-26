# File: app/routes/auth.py
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, logout_user
from app.models.user import User, db
from app.models.notification import UserNotificationSettings

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('ddns.dashboard'))
        flash('Invalid username or password')
    return render_template('auth/login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Check if the username or email already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('auth.register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already exists')
            return redirect(url_for('auth.register'))
        
        # Create a new user
        user = User(username=username, email=email)
        user.set_password(password)
        
        # Add the user to the session and commit, so it gets an ID
        db.session.add(user)
        db.session.commit()  # This will assign the user.id
        
        # Now that the user is committed and has an ID, create notification settings
        user_notification_settings = UserNotificationSettings(user_id=user.id)
        db.session.add(user_notification_settings)
        db.session.commit()
        
        flash('Registered successfully. Please log in.')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html')
