from db import fetch_one, execute
from session import add_message, set_session_cookie_header, create_session


def contact_submit(request):
    """POST - Handle test drive request form submission"""
    params = request.get('params', {})
    listing = params.get('listing', '')
    listing_id = params.get('listing_id', '')
    name = params.get('name', '')
    email = params.get('email', '')
    phone = params.get('phone', '')
    message = params.get('message', '')
    user_id = params.get('user_id', 0)

    session_id = request.get('session_id')
    if not session_id:
        session_id = create_session(0, 'temp')

    # Check for required fields
    if not all([listing_id, name, email, phone]):
        add_message(session_id, 'danger', 'Please fill in all required fields')
        return {
            'redirect': f'/listings/{listing_id}' if listing_id else '/listings',
            'headers': {'Set-Cookie': set_session_cookie_header(session_id)}
        }

    # Check for duplicate request (same user, same listing)
    if request.get('is_authenticated') and user_id:
        existing = fetch_one(
            "SELECT id FROM contacts_contact WHERE listing_id = %s AND user_id = %s",
            (int(listing_id), int(user_id))
        )
        if existing:
            add_message(session_id, 'danger', 'You have already made a request for this listing')
            return {
                'redirect': f'/listings/{listing_id}',
                'headers': {'Set-Cookie': set_session_cookie_header(session_id)}
            }

    # Insert contact
    try:
        execute(
            "INSERT INTO contacts_contact (listing, listing_id, name, email, phone, message, contact_date, user_id) "
            "VALUES (%s, %s, %s, %s, %s, %s, NOW(), %s)",
            (listing, int(listing_id), name, email, phone, message, int(user_id) if user_id else 0)
        )
        add_message(session_id, 'success',
                     'Your test drive request has been submitted! An advisor will get back to you soon.')
    except Exception as e:
        add_message(session_id, 'danger', 'Something went wrong. Please try again.')
        print(f"Contact form error: {e}")

    return {
        'redirect': f'/listings/{listing_id}',
        'headers': {'Set-Cookie': set_session_cookie_header(session_id)}
    }
