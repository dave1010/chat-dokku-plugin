import os
import unittest
from flask import Flask
from src.auth import auth_bp, check_auth

class TestAuth(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)

        @self.app.route('/test_home')
        def test_home():
            return 'Test Home'
        self.app.config['REDIRECT_ROUTE'] = 'test_home'
        
        self.app.register_blueprint(auth_bp)
        self.client = self.app.test_client()
        os.environ['PSK'] = 'test_psk'

    def test_login_get(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)

    def test_login_post_valid_psk(self):
        response = self.client.post('/login', data={'psk': 'test_psk'})
        self.assertEqual(response.status_code, 302)
        self.assertIn('auth', response.headers.get('Set-Cookie'))

    def test_login_post_invalid_psk(self):
        response = self.client.post('/login', data={'psk': 'invalid_psk'})
        self.assertEqual(response.status_code, 401)

    def test_logout(self):
        response = self.client.get('/logout')
        self.assertEqual(response.status_code, 302)
        self.assertNotIn('test_psk', response.headers.get('Set-Cookie'))

    def test_check_auth_no_auth(self):
        with self.app.test_request_context('/'):
            response = check_auth()
            self.assertEqual(response, ("Unauthorized\n", 401))

    def test_check_auth_valid_auth(self):
        with self.app.test_request_context('/', headers={'Authorization': 'test_psk'}):
            response = check_auth()
            self.assertEqual(response, None)

if __name__ == "__main__":
    unittest.main()
