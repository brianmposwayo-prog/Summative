"""
Simple Flask app to register, view, and update user profiles stored in a JSON file.

Run: python app.py

This file defines the Flask routes and uses `db.py` and `forms.py` for storage
and input validation.
"""
from flask import Flask, render_template, request, redirect, url_for, flash, abort
import os

from db import get_all_users, get_user, add_user, update_user
from forms import RegisterForm, UpdateForm

app = Flask(__name__)
# Secret key for session/flash usage in development. Replace in production.
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET', 'dev-secret-key')


@app.route('/')
def index():
    """Show a list of registered users with links to their profile pages."""
    users = get_all_users()
    return render_template('index.html', users=users)


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Register a new user. On success, redirect to the user's profile."""
    form = RegisterForm(request.form)
    if request.method == 'POST':
        valid, errors = form.validate()
        if valid:
            # Ensure username uniqueness
            if get_user(form.username):
                errors.append('Username already exists. Choose another.')
            else:
                user = {
                    'username': form.username,
                    'full_name': form.full_name,
                    'email': form.email,
                    'age': form.age,
                    'about': form.about,
                }
                add_user(user)
                flash('Registration successful.', 'success')
                return redirect(url_for('profile', username=form.username))
        for e in errors:
            flash(e, 'danger')
    return render_template('register.html', form=form)


@app.route('/profile/<username>')
def profile(username):
    """Display a user's profile. 404 if not found."""
    user = get_user(username)
    if not user:
        abort(404)
    return render_template('profile.html', user=user)


@app.route('/update/<username>', methods=['GET', 'POST'])
def update(username):
    """Update an existing user's profile fields."""
    user = get_user(username)
    if not user:
        abort(404)
    if request.method == 'POST':
        form = UpdateForm(request.form)
        valid, errors = form.validate()
        if valid:
            updated = {
                'username': username,  # username is immutable here
                'full_name': form.full_name,
                'email': form.email,
                'age': form.age,
                'about': form.about,
            }
            update_user(username, updated)
            flash('Profile updated.', 'success')
            return redirect(url_for('profile', username=username))
        for e in errors:
            flash(e, 'danger')
        return render_template('update.html', form=form, user=user)
    else:
        # Pre-fill form with existing data
        form = UpdateForm(data=user)
        return render_template('update.html', form=form, user=user)


if __name__ == '__main__':
    # Development server
    app.run(debug=True)
