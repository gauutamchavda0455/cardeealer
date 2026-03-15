"""
Admin Panel - Pure Python (Django Admin jaisi functionality)
- Dashboard with counts
- Listings: View, Add, Edit, Delete
- Advisors: View, Add, Edit, Delete
- Contacts: View, Delete
"""
import os
import time
import uuid
from db import fetch_all, fetch_one, execute, count
from template_engine import render_template, format_price
from session import (
    create_session, get_session, add_message, get_messages,
    set_session_cookie_header, delete_session_cookie_header
)
from config import MEDIA_DIR


def admin_login_page(request):
    """GET - Admin login form"""
    if _is_admin(request):
        return {'redirect': '/admin/dashboard'}

    messages_html = _build_messages_html(request)
    html = render_template('admin/login.html', {'messages': messages_html})
    return {'status': 200, 'body': html}


def admin_login_submit(request):
    """POST - Admin login"""
    params = request.get('params', {})
    username = params.get('username', '')
    password = params.get('password', '')

    user = fetch_one(
        "SELECT id, username, password, first_name, last_name, email, is_staff, is_superuser "
        "FROM auth_user WHERE username = %s",
        (username,)
    )

    if user and user.get('is_staff') and _check_password(password, user['password']):
        session_id = create_session(
            user['id'], user['username'],
            user.get('first_name', ''), user.get('last_name', ''),
            user.get('email', '')
        )
        # Mark as admin in session
        from session import _sessions
        _sessions[session_id]['is_admin'] = True
        add_message(session_id, 'success', f"Welcome Admin {user['username']}!")
        return {
            'redirect': '/admin/dashboard',
            'headers': {'Set-Cookie': set_session_cookie_header(session_id)}
        }

    temp_sid = create_session(0, 'temp')
    add_message(temp_sid, 'danger', 'Invalid credentials or not an admin user')
    return {
        'redirect': '/admin',
        'headers': {'Set-Cookie': set_session_cookie_header(temp_sid)}
    }


def admin_logout(request):
    """Admin logout"""
    session_id = request.get('session_id')
    if session_id:
        from session import delete_session
        delete_session(session_id)
    return {
        'redirect': '/admin',
        'headers': {'Set-Cookie': delete_session_cookie_header()}
    }


def admin_dashboard(request):
    """Admin dashboard with stats"""
    if not _is_admin(request):
        return {'redirect': '/admin'}

    listing_count = count("SELECT COUNT(*) FROM listings_listing")
    advisor_count = count("SELECT COUNT(*) FROM advisors_advisor")
    contact_count = count("SELECT COUNT(*) FROM contacts_contact")
    user_count = count("SELECT COUNT(*) FROM auth_user")

    messages_html = _build_messages_html(request)

    html = render_template('admin/dashboard.html', {
        'messages': messages_html,
        'listing_count': listing_count,
        'advisor_count': advisor_count,
        'contact_count': contact_count,
        'user_count': user_count,
        'admin_user': request.get('user', {}).get('username', 'Admin'),
    })
    return {'status': 200, 'body': html}


# ==================== LISTINGS ====================

def admin_listings(request):
    """List all listings"""
    if not _is_admin(request):
        return {'redirect': '/admin'}

    listings = fetch_all(
        "SELECT l.*, a.name as advisor_name FROM listings_listing l "
        "LEFT JOIN advisors_advisor a ON l.advisor_id = a.id "
        "ORDER BY l.list_date DESC"
    )

    rows_html = ''
    for l in listings:
        published = '<span class="badge badge-success">Yes</span>' if l['is_published'] else '<span class="badge badge-danger">No</span>'
        rows_html += f'''
        <tr>
          <td>{l['id']}</td>
          <td>{l['vin']}</td>
          <td>{l['year']}</td>
          <td>{l['make']}</td>
          <td>{l['model']}</td>
          <td>{l['color']}</td>
          <td>{l['condition']}</td>
          <td>&#8377; {format_price(l['price'])}</td>
          <td>{l.get('advisor_name', '-')}</td>
          <td>{published}</td>
          <td>
            <a href="/admin/listings/edit/{l['id']}" class="btn btn-sm btn-warning">Edit</a>
            <a href="/admin/listings/delete/{l['id']}" class="btn btn-sm btn-danger" onclick="return confirm('Are you sure?')">Delete</a>
          </td>
        </tr>'''

    messages_html = _build_messages_html(request)
    html = render_template('admin/listings.html', {
        'messages': messages_html,
        'rows': rows_html,
        'count': len(listings),
        'admin_user': request.get('user', {}).get('username', 'Admin'),
    })
    return {'status': 200, 'body': html}


def admin_listing_add_page(request):
    """GET - Add listing form"""
    if not _is_admin(request):
        return {'redirect': '/admin'}

    advisors = fetch_all("SELECT id, name FROM advisors_advisor ORDER BY name")
    advisor_options = ''.join([f'<option value="{a["id"]}">{a["name"]}</option>' for a in advisors])

    messages_html = _build_messages_html(request)
    html = render_template('admin/listing_form.html', {
        'messages': messages_html,
        'form_title': 'Add New Listing',
        'form_action': '/admin/listings/add',
        'advisor_options': advisor_options,
        'vin': '', 'condition_new': '', 'condition_used': '',
        'body_style': '', 'year': '', 'make': '', 'model': '',
        'price': '', 'color': '', 'interior_color': '',
        'drivetrain': '', 'transmission': '', 'fuel': '',
        'mileage': '0', 'description': '',
        'published_checked': 'checked',
        'admin_user': request.get('user', {}).get('username', 'Admin'),
    })
    return {'status': 200, 'body': html}


def admin_listing_add_submit(request):
    """POST - Add listing"""
    if not _is_admin(request):
        return {'redirect': '/admin'}

    p = request.get('params', {})
    session_id = request.get('session_id')

    try:
        is_published = 1 if p.get('is_published') == 'on' else 0
        execute(
            "INSERT INTO listings_listing (advisor_id, vin, `condition`, body_style, year, make, model, "
            "price, color, interior_color, drivetrain, transmission, fuel, mileage, description, "
            "photo_main, photo_1, photo_2, photo_3, photo_4, is_published, list_date, created_at, updated_at) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW(), NOW())",
            (
                int(p.get('advisor_id', 1)), p.get('vin', ''), p.get('condition', ''),
                p.get('body_style', ''), int(p.get('year', 2024)), p.get('make', ''),
                p.get('model', ''), int(p.get('price', 0)), p.get('color', ''),
                p.get('interior_color', ''), p.get('drivetrain', ''),
                p.get('transmission', ''), p.get('fuel', ''),
                int(p.get('mileage', 0)), p.get('description', ''),
                p.get('photo_main', ''), p.get('photo_1', ''), p.get('photo_2', ''),
                p.get('photo_3', ''), p.get('photo_4', ''), is_published,
            )
        )
        add_message(session_id, 'success', 'Listing added successfully!')
    except Exception as e:
        add_message(session_id, 'danger', f'Error adding listing: {e}')

    return {'redirect': '/admin/listings', 'headers': {'Set-Cookie': set_session_cookie_header(session_id)}}


def admin_listing_edit_page(request):
    """GET - Edit listing form"""
    if not _is_admin(request):
        return {'redirect': '/admin'}

    listing_id = request.get('item_id')
    listing = fetch_one("SELECT * FROM listings_listing WHERE id = %s", (listing_id,))
    if not listing:
        return {'redirect': '/admin/listings'}

    advisors = fetch_all("SELECT id, name FROM advisors_advisor ORDER BY name")
    advisor_options = ''.join([
        f'<option value="{a["id"]}" {"selected" if a["id"] == listing["advisor_id"] else ""}>{a["name"]}</option>'
        for a in advisors
    ])

    messages_html = _build_messages_html(request)
    html = render_template('admin/listing_form.html', {
        'messages': messages_html,
        'form_title': f'Edit Listing: {listing["year"]} {listing["make"]} {listing["model"]}',
        'form_action': f'/admin/listings/edit/{listing_id}',
        'advisor_options': advisor_options,
        'vin': listing['vin'],
        'condition_new': 'selected' if listing['condition'] == 'New' else '',
        'condition_used': 'selected' if listing['condition'] == 'Used' else '',
        'body_style': listing['body_style'],
        'year': listing['year'],
        'make': listing['make'],
        'model': listing['model'],
        'price': listing['price'],
        'color': listing['color'],
        'interior_color': listing['interior_color'],
        'drivetrain': listing['drivetrain'],
        'transmission': listing['transmission'],
        'fuel': listing['fuel'],
        'mileage': listing['mileage'],
        'description': listing['description'] or '',
        'published_checked': 'checked' if listing['is_published'] else '',
        'admin_user': request.get('user', {}).get('username', 'Admin'),
    })
    return {'status': 200, 'body': html}


def admin_listing_edit_submit(request):
    """POST - Update listing"""
    if not _is_admin(request):
        return {'redirect': '/admin'}

    listing_id = request.get('item_id')
    p = request.get('params', {})
    session_id = request.get('session_id')

    try:
        is_published = 1 if p.get('is_published') == 'on' else 0
        execute(
            "UPDATE listings_listing SET advisor_id=%s, vin=%s, `condition`=%s, body_style=%s, "
            "year=%s, make=%s, model=%s, price=%s, color=%s, interior_color=%s, "
            "drivetrain=%s, transmission=%s, fuel=%s, mileage=%s, description=%s, "
            "is_published=%s, updated_at=NOW() WHERE id=%s",
            (
                int(p.get('advisor_id', 1)), p.get('vin', ''), p.get('condition', ''),
                p.get('body_style', ''), int(p.get('year', 2024)), p.get('make', ''),
                p.get('model', ''), int(p.get('price', 0)), p.get('color', ''),
                p.get('interior_color', ''), p.get('drivetrain', ''),
                p.get('transmission', ''), p.get('fuel', ''),
                int(p.get('mileage', 0)), p.get('description', ''),
                is_published, listing_id,
            )
        )
        add_message(session_id, 'success', 'Listing updated successfully!')
    except Exception as e:
        add_message(session_id, 'danger', f'Error updating listing: {e}')

    return {'redirect': '/admin/listings', 'headers': {'Set-Cookie': set_session_cookie_header(session_id)}}


def admin_listing_delete(request):
    """Delete a listing"""
    if not _is_admin(request):
        return {'redirect': '/admin'}

    listing_id = request.get('item_id')
    session_id = request.get('session_id')

    try:
        execute("DELETE FROM listings_listing WHERE id = %s", (listing_id,))
        add_message(session_id, 'success', 'Listing deleted successfully!')
    except Exception as e:
        add_message(session_id, 'danger', f'Error deleting listing: {e}')

    return {'redirect': '/admin/listings', 'headers': {'Set-Cookie': set_session_cookie_header(session_id)}}


# ==================== ADVISORS ====================

def admin_advisors(request):
    """List all advisors"""
    if not _is_admin(request):
        return {'redirect': '/admin'}

    advisors = fetch_all("SELECT * FROM advisors_advisor ORDER BY hire_date DESC")

    rows_html = ''
    for a in advisors:
        mvp = '<span class="badge badge-warning">MVP</span>' if a['is_mvp'] else ''
        rows_html += f'''
        <tr>
          <td>{a['id']}</td>
          <td>{a['name']}</td>
          <td>{a['email']}</td>
          <td>{a['phone']}</td>
          <td>{a['hire_date']}</td>
          <td>{mvp}</td>
          <td>
            <a href="/admin/advisors/edit/{a['id']}" class="btn btn-sm btn-warning">Edit</a>
            <a href="/admin/advisors/delete/{a['id']}" class="btn btn-sm btn-danger" onclick="return confirm('Are you sure?')">Delete</a>
          </td>
        </tr>'''

    messages_html = _build_messages_html(request)
    html = render_template('admin/advisors.html', {
        'messages': messages_html,
        'rows': rows_html,
        'count': len(advisors),
        'admin_user': request.get('user', {}).get('username', 'Admin'),
    })
    return {'status': 200, 'body': html}


def admin_advisor_add_page(request):
    """GET - Add advisor form"""
    if not _is_admin(request):
        return {'redirect': '/admin'}

    messages_html = _build_messages_html(request)
    html = render_template('admin/advisor_form.html', {
        'messages': messages_html,
        'form_title': 'Add New Advisor',
        'form_action': '/admin/advisors/add',
        'name': '', 'phone': '', 'email': '',
        'description': '', 'mvp_checked': '',
        'admin_user': request.get('user', {}).get('username', 'Admin'),
    })
    return {'status': 200, 'body': html}


def admin_advisor_add_submit(request):
    """POST - Add advisor"""
    if not _is_admin(request):
        return {'redirect': '/admin'}

    p = request.get('params', {})
    session_id = request.get('session_id')

    try:
        is_mvp = 1 if p.get('is_mvp') == 'on' else 0
        execute(
            "INSERT INTO advisors_advisor (name, photo, description, phone, email, is_mvp, hire_date, created_at, updated_at) "
            "VALUES (%s, %s, %s, %s, %s, %s, NOW(), NOW(), NOW())",
            (p.get('name', ''), p.get('photo', ''), p.get('description', ''),
             p.get('phone', ''), p.get('email', ''), is_mvp)
        )
        add_message(session_id, 'success', 'Advisor added successfully!')
    except Exception as e:
        add_message(session_id, 'danger', f'Error adding advisor: {e}')

    return {'redirect': '/admin/advisors', 'headers': {'Set-Cookie': set_session_cookie_header(session_id)}}


def admin_advisor_edit_page(request):
    """GET - Edit advisor form"""
    if not _is_admin(request):
        return {'redirect': '/admin'}

    advisor_id = request.get('item_id')
    advisor = fetch_one("SELECT * FROM advisors_advisor WHERE id = %s", (advisor_id,))
    if not advisor:
        return {'redirect': '/admin/advisors'}

    messages_html = _build_messages_html(request)
    html = render_template('admin/advisor_form.html', {
        'messages': messages_html,
        'form_title': f'Edit Advisor: {advisor["name"]}',
        'form_action': f'/admin/advisors/edit/{advisor_id}',
        'name': advisor['name'],
        'phone': advisor['phone'],
        'email': advisor['email'],
        'description': advisor['description'] or '',
        'mvp_checked': 'checked' if advisor['is_mvp'] else '',
        'admin_user': request.get('user', {}).get('username', 'Admin'),
    })
    return {'status': 200, 'body': html}


def admin_advisor_edit_submit(request):
    """POST - Update advisor"""
    if not _is_admin(request):
        return {'redirect': '/admin'}

    advisor_id = request.get('item_id')
    p = request.get('params', {})
    session_id = request.get('session_id')

    try:
        is_mvp = 1 if p.get('is_mvp') == 'on' else 0
        execute(
            "UPDATE advisors_advisor SET name=%s, description=%s, phone=%s, email=%s, "
            "is_mvp=%s, updated_at=NOW() WHERE id=%s",
            (p.get('name', ''), p.get('description', ''), p.get('phone', ''),
             p.get('email', ''), is_mvp, advisor_id)
        )
        add_message(session_id, 'success', 'Advisor updated successfully!')
    except Exception as e:
        add_message(session_id, 'danger', f'Error updating advisor: {e}')

    return {'redirect': '/admin/advisors', 'headers': {'Set-Cookie': set_session_cookie_header(session_id)}}


def admin_advisor_delete(request):
    """Delete an advisor"""
    if not _is_admin(request):
        return {'redirect': '/admin'}

    advisor_id = request.get('item_id')
    session_id = request.get('session_id')

    try:
        execute("DELETE FROM advisors_advisor WHERE id = %s", (advisor_id,))
        add_message(session_id, 'success', 'Advisor deleted successfully!')
    except Exception as e:
        add_message(session_id, 'danger', f'Error deleting advisor: {e}')

    return {'redirect': '/admin/advisors', 'headers': {'Set-Cookie': set_session_cookie_header(session_id)}}


# ==================== CONTACTS ====================

def admin_contacts(request):
    """List all contacts/test drive requests"""
    if not _is_admin(request):
        return {'redirect': '/admin'}

    contacts = fetch_all("SELECT * FROM contacts_contact ORDER BY contact_date DESC")

    rows_html = ''
    for c in contacts:
        rows_html += f'''
        <tr>
          <td>{c['id']}</td>
          <td>{c['name']}</td>
          <td>{c['listing']}</td>
          <td>{c['email']}</td>
          <td>{c['phone']}</td>
          <td>{c['contact_date']}</td>
          <td>
            <a href="/admin/contacts/delete/{c['id']}" class="btn btn-sm btn-danger" onclick="return confirm('Are you sure?')">Delete</a>
          </td>
        </tr>'''

    messages_html = _build_messages_html(request)
    html = render_template('admin/contacts.html', {
        'messages': messages_html,
        'rows': rows_html,
        'count': len(contacts),
        'admin_user': request.get('user', {}).get('username', 'Admin'),
    })
    return {'status': 200, 'body': html}


def admin_contact_delete(request):
    """Delete a contact"""
    if not _is_admin(request):
        return {'redirect': '/admin'}

    contact_id = request.get('item_id')
    session_id = request.get('session_id')

    try:
        execute("DELETE FROM contacts_contact WHERE id = %s", (contact_id,))
        add_message(session_id, 'success', 'Contact deleted!')
    except Exception as e:
        add_message(session_id, 'danger', f'Error: {e}')

    return {'redirect': '/admin/contacts', 'headers': {'Set-Cookie': set_session_cookie_header(session_id)}}


# ==================== HELPERS ====================

def _is_admin(request):
    session = request.get('session')
    return session and session.get('is_admin', False)


def _check_password(raw_password, stored_hash):
    if not stored_hash or '$' not in stored_hash:
        return False
    try:
        algorithm, iterations, salt, hash_val = stored_hash.split('$', 3)
        if algorithm == 'pbkdf2_sha256':
            import hashlib
            import base64
            dk = hashlib.pbkdf2_hmac('sha256', raw_password.encode(), salt.encode(), int(iterations))
            computed = base64.b64encode(dk).decode('ascii')
            return computed == hash_val
    except (ValueError, KeyError):
        pass
    return False


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
        <div class="alert alert-{msg['type']} alert-dismissible fade show mx-3 mt-2" role="alert">
          {msg['text']}
          <button type="button" class="close" data-dismiss="alert"><span>&times;</span></button>
        </div>'''
    return html
