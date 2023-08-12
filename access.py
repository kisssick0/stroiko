from functools import wraps

from flask import session, render_template, current_app, request, redirect, url_for


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'id' in session:
            return func(*args, **kwargs)
        return redirect(url_for('blueprint_auth.auth'))
    return wrapper


def group_validation(config: dict) -> bool:
    endpoint_func = request.endpoint
    endpoint_app = request.endpoint.split('.')[0]
    if 'role' in session:
        user_group = session['role']
        if user_group in config and endpoint_app in config[user_group]:
            return True
        elif user_group in config and endpoint_func in config[user_group]:
            return True
    return False


def group_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        config = current_app.config['access_config']
        if group_validation(config):
            return f(*args, **kwargs)
        return "error not access"
    return wrapper


def external_validation(config):
    endpoint_app = request.endpoint.split('.')[0]
    user_id = session.get('user_id', None)
    user_group = session.get('user_group', None)
    if user_id and user_group is None:
        if endpoint_app in config['external']:
            return True
    return False


def external_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        config = current_app.config['access_config']
        if external_validation(config):
            return f(*args, **kwargs)
        return render_template('exceptions/external_only.html')
    return wrapper
