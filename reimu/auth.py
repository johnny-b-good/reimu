from flask import Blueprint, g, render_template, abort, redirect, url_for, request, current_app, session

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET'])
def login_page():
    """Render the login page."""
    if session.get('is_admin', False):
        return redirect(url_for('admin.posts_page'))
    else:    
        return render_template('auth.html')


@auth.route('/login', methods=['POST'])
def login():
    """Login as blog admin."""

    # Successeful login conditions
    user_is_valid = request.form['user'] == current_app.config['USER']
    password_is_valid = request.form['password'] == current_app.config['PASSWORD']
    trap_is_empty = not request.form['trap']

    # Login user if credentials are correct
    if user_is_valid and password_is_valid and trap_is_empty:
        session['is_admin'] = True
        return redirect(url_for('admin.posts_page'))
    else:
        return render_template('auth.html')


@auth.route('/logout', methods=['GET', 'POST'])
def logout():
    """Logout."""
    session.pop('is_admin', None)
    return redirect(url_for('blog.index_page'))
