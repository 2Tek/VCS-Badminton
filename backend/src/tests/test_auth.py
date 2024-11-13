
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

print("Python Path:", sys.path)

import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from auth.auth import get_token_auth_header, check_permissions, verify_decode_jwt, AuthError


# Initialize Flask app for request context
app = Flask(__name__)

@pytest.fixture
def client():
    with app.test_request_context():
        yield app.test_client()

def test_get_token_auth_header_missing(client):
    """Test missing Authorization header"""
    with pytest.raises(AuthError) as excinfo:
        get_token_auth_header()
    assert excinfo.value.error['code'] == 'authorization_header_missing'

def test_get_token_auth_header_invalid_format(client):
    """Test Authorization header with invalid format"""
    with patch('flask.request') as mock_request:
        mock_request.headers = {'Authorization': 'InvalidToken'}
        with pytest.raises(AuthError) as excinfo:
            get_token_auth_header()
    assert excinfo.value.error['code'] == 'invalid_header'

def test_check_permissions_valid():
    """Test valid permissions"""
    payload = {'permissions': ['read:data']}
    assert check_permissions('read:data', payload) is True

def test_check_permissions_invalid():
    """Test invalid permissions"""
    payload = {'permissions': ['read:data']}
    with pytest.raises(AuthError) as excinfo:
        check_permissions('write:data', payload)
    assert excinfo.value.error['code'] == 'unauthorized'

def test_verify_decode_jwt_invalid_token():
    """Test decoding invalid JWT"""
    with pytest.raises(AuthError) as excinfo:
        verify_decode_jwt("invalid.token")
    assert excinfo.value.error['code'] == 'invalid_header'

@patch('src.auth.auth.urlopen')
@patch('src.auth.auth.jwt.decode')
def test_verify_decode_jwt_valid(mock_jwt_decode, mock_urlopen):
    """Test decoding a valid JWT"""
    # Mock the response from Auth0
    mock_urlopen.return_value = MagicMock()
    mock_urlopen.return_value.read.return_value = json.dumps({
        'keys': [{'kid': '1234', 'kty': 'RSA', 'use': 'sig', 'n': '...', 'e': 'AQAB'}]
    })

    # Mock payload decoding
    mock_jwt_decode.return_value = {'permissions': ['read:data']}

    token = "valid.token.here"
    payload = verify_decode_jwt(token)
    assert payload == {'permissions': ['read:data']}
