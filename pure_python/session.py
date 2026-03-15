import uuid
import time
import hashlib
from http.cookies import SimpleCookie
from config import SESSION_COOKIE_NAME, SESSION_EXPIRY, SECRET_KEY

# In-memory session store
_sessions = {}


def create_session(user_id, username, first_name='', last_name='', email=''):
    session_id = hashlib.sha256(
        f"{uuid.uuid4()}{SECRET_KEY}{time.time()}".encode()
    ).hexdigest()

    _sessions[session_id] = {
        'user_id': user_id,
        'username': username,
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'is_authenticated': True,
        'created_at': time.time(),
        'messages': [],  # flash messages
    }
    return session_id


def get_session(session_id):
    if not session_id or session_id not in _sessions:
        return None
    session = _sessions[session_id]
    # Check expiry
    if time.time() - session['created_at'] > SESSION_EXPIRY:
        del _sessions[session_id]
        return None
    return session


def delete_session(session_id):
    if session_id in _sessions:
        del _sessions[session_id]


def get_session_id_from_cookie(cookie_header):
    if not cookie_header:
        return None
    cookie = SimpleCookie()
    cookie.load(cookie_header)
    if SESSION_COOKIE_NAME in cookie:
        return cookie[SESSION_COOKIE_NAME].value
    return None


def set_session_cookie_header(session_id):
    return f"{SESSION_COOKIE_NAME}={session_id}; Path=/; HttpOnly; Max-Age={SESSION_EXPIRY}"


def delete_session_cookie_header():
    return f"{SESSION_COOKIE_NAME}=; Path=/; HttpOnly; Max-Age=0"


def add_message(session_id, msg_type, text):
    """Add a flash message. msg_type: 'success', 'danger', 'info', 'warning'"""
    session = get_session(session_id)
    if session:
        session['messages'].append({'type': msg_type, 'text': text})


def get_messages(session_id):
    """Get and clear flash messages."""
    session = get_session(session_id)
    if session:
        messages = session['messages']
        session['messages'] = []
        return messages
    return []
