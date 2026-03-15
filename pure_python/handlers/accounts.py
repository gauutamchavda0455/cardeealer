import hashlib
from db import fetch_all, fetch_one, execute
from template_engine import render_template
from session import (
    create_session, delete_session, add_message, get_messages,
    set_session_cookie_header, delete_session_cookie_header
)


def login_page(request):
    """GET - Show login form"""
    if request.get('is_authenticated'):
        return {'redirect': '/accounts/dashboard'}

    messages_html = _build_messages_html(request)

    html = render_template('login.html', {
        'messages': messages_html,
        'is_authenticated': '',
        'username': '',
        'first_name': '',
        'nav_home_active': '',
        'nav_about_active': '',
        'nav_listings_active': '',
    })
    return {'status': 200, 'body': html}


def login_submit(request):
    """POST - Process login"""
    params = request.get('params', {})
    username = params.get('username', '')
    password = params.get('password', '')

    if not username or not password:
        session_id = request.get('session_id')
        if session_id:
            add_message(session_id, 'danger', 'Please fill in all fields')
        return {'redirect': '/accounts/login'}

    # Check user in Django's auth_user table
    user = fetch_one(
        "SELECT id, username, password, first_name, last_name, email, is_active "
        "FROM auth_user WHERE username = %s",
        (username,)
    )

    if user and _check_django_password(password, user['password']):
        if not user.get('is_active', True):
            # Create temp session for message
            temp_sid = create_session(0, 'temp')
            add_message(temp_sid, 'danger', 'Account is disabled')
            return {
                'redirect': '/accounts/login',
                'headers': {'Set-Cookie': set_session_cookie_header(temp_sid)}
            }

        session_id = create_session(
            user['id'], user['username'],
            user.get('first_name', ''), user.get('last_name', ''),
            user.get('email', '')
        )
        add_message(session_id, 'success', f"Welcome back, {user.get('first_name', user['username'])}!")
        return {
            'redirect': '/accounts/dashboard',
            'headers': {'Set-Cookie': set_session_cookie_header(session_id)}
        }
    else:
        # Create temp session for error message
        temp_sid = create_session(0, 'temp')
        add_message(temp_sid, 'danger', 'Invalid username or password')
        return {
            'redirect': '/accounts/login',
            'headers': {'Set-Cookie': set_session_cookie_header(temp_sid)}
        }


def register_page(request):
    """GET - Show register form"""
    if request.get('is_authenticated'):
        return {'redirect': '/accounts/dashboard'}

    messages_html = _build_messages_html(request)

    html = render_template('register.html', {
        'messages': messages_html,
        'is_authenticated': '',
        'username': '',
        'first_name': '',
        'nav_home_active': '',
        'nav_about_active': '',
        'nav_listings_active': '',
    })
    return {'status': 200, 'body': html}


def register_submit(request):
    """POST - Process registration"""
    params = request.get('params', {})
    first_name = params.get('first_name', '')
    last_name = params.get('last_name', '')
    username = params.get('username', '')
    email = params.get('email', '')
    password = params.get('password', '')
    password2 = params.get('password2', '')

    # Create temp session for messages
    temp_sid = request.get('session_id')
    if not temp_sid:
        temp_sid = create_session(0, 'temp')

    # Validation
    if not all([first_name, last_name, username, email, password, password2]):
        add_message(temp_sid, 'danger', 'Please fill in all fields')
        return {
            'redirect': '/accounts/register',
            'headers': {'Set-Cookie': set_session_cookie_header(temp_sid)}
        }

    if password != password2:
        add_message(temp_sid, 'danger', 'Passwords do not match')
        return {
            'redirect': '/accounts/register',
            'headers': {'Set-Cookie': set_session_cookie_header(temp_sid)}
        }

    if len(password) < 8:
        add_message(temp_sid, 'danger', 'Password must be at least 8 characters')
        return {
            'redirect': '/accounts/register',
            'headers': {'Set-Cookie': set_session_cookie_header(temp_sid)}
        }

    # Check existing user
    existing = fetch_one("SELECT id FROM auth_user WHERE username = %s", (username,))
    if existing:
        add_message(temp_sid, 'danger', 'Username already exists')
        return {
            'redirect': '/accounts/register',
            'headers': {'Set-Cookie': set_session_cookie_header(temp_sid)}
        }

    existing_email = fetch_one("SELECT id FROM auth_user WHERE email = %s", (email,))
    if existing_email:
        add_message(temp_sid, 'danger', 'Email already registered')
        return {
            'redirect': '/accounts/register',
            'headers': {'Set-Cookie': set_session_cookie_header(temp_sid)}
        }

    # Create user (Django-compatible password hash)
    hashed_password = _make_django_password(password)
    user_id = execute(
        "INSERT INTO auth_user (password, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) "
        "VALUES (%s, 0, %s, %s, %s, %s, 0, 1, NOW())",
        (hashed_password, username, first_name, last_name, email)
    )

    # Auto login
    session_id = create_session(user_id, username, first_name, last_name, email)
    add_message(session_id, 'success', f'Welcome {first_name}! You are now registered.')

    return {
        'redirect': '/accounts/dashboard',
        'headers': {'Set-Cookie': set_session_cookie_header(session_id)}
    }


def logout(request):
    """Logout user"""
    session_id = request.get('session_id')
    if session_id:
        delete_session(session_id)

    return {
        'redirect': '/',
        'headers': {'Set-Cookie': delete_session_cookie_header()}
    }


def dashboard(request):
    """User dashboard - show test drive requests"""
    if not request.get('is_authenticated'):
        return {'redirect': '/accounts/login'}

    user = request.get('user', {})
    user_id = user.get('user_id')

    # Get user's test drive requests
    contacts = fetch_all(
        "SELECT * FROM contacts_contact WHERE user_id = %s ORDER BY contact_date DESC",
        (user_id,)
    )

    requests_html = ''
    if contacts:
        for c in contacts:
            requests_html += f'''
            <tr>
              <td>{c['listing']}</td>
              <td><a href="/listings/{c['listing_id']}">{c['listing_id']}</a></td>
              <td>{c['contact_date']}</td>
            </tr>'''
    else:
        requests_html = '<tr><td colspan="3" class="text-center">No test drive requests yet</td></tr>'

    messages_html = _build_messages_html(request)

    html = render_template('dashboard.html', {
        'first_name': user.get('first_name', ''),
        'username': user.get('username', ''),
        'requests': requests_html,
        'messages': messages_html,
        'is_authenticated': 'true',
        'nav_home_active': '',
        'nav_about_active': '',
        'nav_listings_active': '',
    })

    return {'status': 200, 'body': html}


def _check_django_password(raw_password, stored_hash):
    """Check password against Django's PBKDF2 hash format."""
    if not stored_hash or '$' not in stored_hash:
        return False
    try:
        algorithm, iterations, salt, hash_val = stored_hash.split('$', 3)
        if algorithm == 'pbkdf2_sha256':
            import hashlib as hl
            dk = hl.pbkdf2_hmac(
                'sha256',
                raw_password.encode('utf-8'),
                salt.encode('utf-8'),
                int(iterations)
            )
            import base64
            computed = base64.b64encode(dk).decode('ascii')
            return computed == hash_val
    except (ValueError, KeyError):
        pass
    return False


def _make_django_password(raw_password):
    """Create a Django-compatible PBKDF2 password hash."""
    import os
    import base64
    salt = base64.b64encode(os.urandom(12)).decode('ascii')
    iterations = 600000
    dk = hashlib.pbkdf2_hmac(
        'sha256',
        raw_password.encode('utf-8'),
        salt.encode('utf-8'),
        iterations
    )
    hash_val = base64.b64encode(dk).decode('ascii')
    return f"pbkdf2_sha256${iterations}${salt}${hash_val}"


def _build_messages_html(request):
    session_id = request.get('session_id')
    if not session_id:
        return ''
    messages = get_messages(session_id)
    if not messages:
        return ''
    html = ''
    for msg in messages:
        html += f'''
        <div class="container">
          <div class="alert alert-{msg['type']} alert-dismissible fade show" role="alert">
            {msg['text']}
            <button type="button" class="close" data-dismiss="alert"><span>&times;</span></button>
          </div>
        </div>'''
    return html
