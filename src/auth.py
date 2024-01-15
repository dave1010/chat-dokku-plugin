import os
from flask import Blueprint, request, make_response, redirect, url_for, current_app

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        psk = request.form.get('psk')
        if psk == os.environ.get('PSK'):
            redirect_route = current_app.config.get('REDIRECT_ROUTE', 'home')
            resp = make_response(redirect(url_for(redirect_route)))
            resp.set_cookie('auth', psk, secure=True, httponly=True)
            return resp
        else:
            return "Invalid PSK", 401
    return '''
        <form method="post">
            Enter PSK: <input type="password" name="psk">
            <input type="submit">
        </form>
    '''

@auth_bp.route('/logout')
def logout():
    resp = make_response(redirect(url_for('auth.login')))
    resp.delete_cookie('auth')
    return resp

def check_auth():
    psk = os.environ.get('PSK')
    if psk == None:
        return "Auth not configured\n", 500

    if request.endpoint == 'auth.login':
        return None

    # public endpoints
    view_func = current_app.view_functions.get(request.endpoint)
    if view_func and getattr(view_func, 'is_public', False):
        return None

    # CORS
    if request.method == 'OPTIONS':
        return None

    auth_header = request.headers.get('Authorization')
    auth_cookie = request.cookies.get('auth')

    if auth_header != psk and auth_cookie != psk:
        return "Unauthorized\n", 401
