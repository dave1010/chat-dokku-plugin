import os
from flask import Blueprint, request, make_response, redirect, url_for

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        psk = request.form.get('psk')
        if psk == os.environ.get('PSK'):
            resp = make_response(redirect(url_for('home')))
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

    auth_header = request.headers.get('Authorization')
    auth_cookie = request.cookies.get('auth')

    if auth_header != psk and auth_cookie != psk:
        return "Unauthorized\n", 401
