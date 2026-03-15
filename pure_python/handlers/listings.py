import math
from db import fetch_all, fetch_one, count
from template_engine import render_template, format_price, build_options_html, build_pagination_html
from session import get_messages
from config import LISTINGS_PER_PAGE


def index(request):
    """All listings page with pagination"""
    params = request.get('params', {})
    page = int(params.get('page', ['1'])[0]) if isinstance(params.get('page'), list) else int(params.get('page', 1))

    total = count("SELECT COUNT(*) FROM listings_listing WHERE is_published=1")
    total_pages = math.ceil(total / LISTINGS_PER_PAGE)
    offset = (page - 1) * LISTINGS_PER_PAGE

    listings = fetch_all(
        "SELECT * FROM listings_listing WHERE is_published=1 ORDER BY list_date DESC LIMIT %s OFFSET %s",
        (LISTINGS_PER_PAGE, offset)
    )

    cars_html = _build_listing_cards(listings)
    pagination = build_pagination_html(page, total_pages, '/listings')
    messages_html = _build_messages_html(request)
    is_auth = request.get('is_authenticated', False)
    user = request.get('user', {})

    html = render_template('listings.html', {
        'listings': cars_html,
        'pagination': pagination,
        'messages': messages_html,
        'is_authenticated': 'true' if is_auth else '',
        'username': user.get('username', ''),
        'first_name': user.get('first_name', ''),
        'nav_home_active': '',
        'nav_about_active': '',
        'nav_listings_active': 'active',
    })

    return {'status': 200, 'body': html}


def detail(request):
    """Single listing detail page"""
    listing_id = request.get('listing_id')
    listing = fetch_one(
        "SELECT l.*, a.name as advisor_name, a.photo as advisor_photo, a.phone as advisor_phone, a.email as advisor_email "
        "FROM listings_listing l "
        "LEFT JOIN advisors_advisor a ON l.advisor_id = a.id "
        "WHERE l.id = %s",
        (listing_id,)
    )

    if not listing:
        return {'status': 404, 'body': '<h1>Listing Not Found</h1>'}

    # Build photo gallery
    photos_html = ''
    for i in range(1, 5):
        photo = listing.get(f'photo_{i}')
        if photo:
            photos_html += f'''
            <div class="col-md-3 mb-3">
              <a href="/media/{photo}" data-lightbox="car-photos">
                <img src="/media/{photo}" class="img-fluid" alt="Photo {i}">
              </a>
            </div>'''

    # Advisor card
    advisor_html = ''
    if listing.get('advisor_name'):
        advisor_html = f'''
        <div class="card mb-3">
          <img class="card-img-top" src="/media/{listing['advisor_photo']}" alt="{listing['advisor_name']}">
          <div class="card-body">
            <h5 class="card-title">{listing['advisor_name']}</h5>
            <p class="card-text"><i class="fas fa-phone"></i> {listing['advisor_phone']}</p>
            <p class="card-text"><i class="fas fa-envelope"></i> {listing['advisor_email']}</p>
          </div>
        </div>'''

    messages_html = _build_messages_html(request)
    is_auth = request.get('is_authenticated', False)
    user = request.get('user', {})

    html = render_template('listing_detail.html', {
        'id': listing['id'],
        'title': f"{listing['year']} {listing['make']} {listing['model']}",
        'year': listing['year'],
        'make': listing['make'],
        'model': listing['model'],
        'price': format_price(listing['price']),
        'condition': listing['condition'],
        'body_style': listing['body_style'],
        'color': listing['color'],
        'interior_color': listing['interior_color'],
        'drivetrain': listing['drivetrain'],
        'transmission': listing['transmission'],
        'fuel': listing['fuel'],
        'mileage': format_price(listing['mileage']),
        'vin': listing['vin'],
        'description': listing['description'] or '',
        'photo_main': listing['photo_main'],
        'photos': photos_html,
        'advisor': advisor_html,
        'messages': messages_html,
        'is_authenticated': 'true' if is_auth else '',
        'username': user.get('username', ''),
        'first_name': user.get('first_name', ''),
        'user_name': f"{user.get('first_name', '')} {user.get('last_name', '')}".strip(),
        'user_email': user.get('email', ''),
        'user_id': user.get('user_id', ''),
        'nav_home_active': '',
        'nav_about_active': '',
        'nav_listings_active': 'active',
    })

    return {'status': 200, 'body': html}


def search(request):
    """Search listings with filters"""
    params = request.get('params', {})

    def get_param(key):
        val = params.get(key, [''])[0] if isinstance(params.get(key), list) else params.get(key, '')
        return val

    condition = get_param('condition')
    make = get_param('make')
    body_style = get_param('body_style')
    fuel = get_param('fuel')
    transmission = get_param('transmission')
    price = get_param('price')

    # Build query
    sql = "SELECT * FROM listings_listing WHERE is_published=1"
    query_params = []

    if condition:
        sql += " AND condition = %s"
        query_params.append(condition)
    if make:
        sql += " AND make = %s"
        query_params.append(make)
    if body_style:
        sql += " AND body_style = %s"
        query_params.append(body_style)
    if fuel:
        sql += " AND fuel = %s"
        query_params.append(fuel)
    if transmission:
        sql += " AND transmission = %s"
        query_params.append(transmission)
    if price:
        try:
            sql += " AND price <= %s"
            query_params.append(int(price))
        except ValueError:
            pass

    sql += " ORDER BY list_date DESC"
    listings = fetch_all(sql, tuple(query_params))

    cars_html = _build_listing_cards(listings)

    # Search form options
    makes = fetch_all("SELECT DISTINCT make FROM listings_listing WHERE is_published=1 ORDER BY make")
    body_styles = fetch_all("SELECT DISTINCT body_style FROM listings_listing WHERE is_published=1 ORDER BY body_style")
    fuels = fetch_all("SELECT DISTINCT fuel FROM listings_listing WHERE is_published=1 ORDER BY fuel")
    transmissions_list = fetch_all("SELECT DISTINCT transmission FROM listings_listing WHERE is_published=1 ORDER BY transmission")

    messages_html = _build_messages_html(request)
    is_auth = request.get('is_authenticated', False)
    user = request.get('user', {})

    html = render_template('search.html', {
        'listings': cars_html,
        'result_count': len(listings),
        'condition_new': 'selected' if condition == 'New' else '',
        'condition_used': 'selected' if condition == 'Used' else '',
        'make_options': build_options_html([m['make'] for m in makes], make),
        'body_style_options': build_options_html([b['body_style'] for b in body_styles], body_style),
        'fuel_options': build_options_html([f['fuel'] for f in fuels], fuel),
        'transmission_options': build_options_html([t['transmission'] for t in transmissions_list], transmission),
        'price_value': price,
        'messages': messages_html,
        'is_authenticated': 'true' if is_auth else '',
        'username': user.get('username', ''),
        'first_name': user.get('first_name', ''),
        'nav_home_active': '',
        'nav_about_active': '',
        'nav_listings_active': 'active',
    })

    return {'status': 200, 'body': html}


def _build_listing_cards(listings):
    html = ''
    for car in listings:
        html += f'''
        <div class="col-md-4 mb-4">
          <div class="card listing-card">
            <img class="card-img-top" src="/media/{car['photo_main']}" alt="{car['make']} {car['model']}">
            <div class="card-img-overlay">
              <h2><span class="badge badge-dark text-white">&#8377; {format_price(car['price'])}</span></h2>
            </div>
            <div class="card-body">
              <h4 class="card-title">{car['year']} {car['make']} {car['model']}</h4>
              <p class="card-text text-muted">
                <i class="fas fa-road"></i> {format_price(car['mileage'])} Km
                <span class="ml-2"><i class="fas fa-cog"></i> {car['transmission']}</span>
                <span class="ml-2"><i class="fas fa-gas-pump"></i> {car['fuel']}</span>
              </p>
              <a href="/listings/{car['id']}" class="btn btn-dark btn-block">More Info</a>
            </div>
          </div>
        </div>'''
    return html


def _build_messages_html(request):
    session_id = request.get('session_id')
    if not session_id:
        return ''
    from session import get_messages
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
