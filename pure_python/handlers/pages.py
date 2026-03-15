from db import fetch_all, fetch_one
from template_engine import render_template, format_price, build_options_html
from session import get_messages


def index(request):
    """Home page - featured listings + search form"""
    # Get 3 latest published listings
    listings = fetch_all(
        "SELECT * FROM listings_listing WHERE is_published=1 ORDER BY list_date DESC LIMIT 3"
    )

    # Build featured cars HTML
    cars_html = ''
    for car in listings:
        cars_html += f'''
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

    # Get unique values for search form dropdowns
    makes = fetch_all("SELECT DISTINCT make FROM listings_listing WHERE is_published=1 ORDER BY make")
    body_styles = fetch_all("SELECT DISTINCT body_style FROM listings_listing WHERE is_published=1 ORDER BY body_style")
    fuels = fetch_all("SELECT DISTINCT fuel FROM listings_listing WHERE is_published=1 ORDER BY fuel")
    transmissions = fetch_all("SELECT DISTINCT transmission FROM listings_listing WHERE is_published=1 ORDER BY transmission")

    make_options = build_options_html([m['make'] for m in makes])
    body_options = build_options_html([b['body_style'] for b in body_styles])
    fuel_options = build_options_html([f['fuel'] for f in fuels])
    trans_options = build_options_html([t['transmission'] for t in transmissions])

    # Messages
    messages_html = _build_messages_html(request)

    # Auth context
    is_auth = request.get('is_authenticated', False)
    user = request.get('user', {})

    html = render_template('index.html', {
        'featured_cars': cars_html,
        'make_options': make_options,
        'body_style_options': body_options,
        'fuel_options': fuel_options,
        'transmission_options': trans_options,
        'messages': messages_html,
        'is_authenticated': 'true' if is_auth else '',
        'username': user.get('username', ''),
        'first_name': user.get('first_name', ''),
        'nav_home_active': 'active',
        'nav_about_active': '',
        'nav_listings_active': '',
    })

    return {'status': 200, 'body': html}


def about(request):
    """About page - advisors + MVP"""
    advisors = fetch_all("SELECT * FROM advisors_advisor ORDER BY hire_date DESC")
    mvp = fetch_one("SELECT * FROM advisors_advisor WHERE is_mvp=1 LIMIT 1")

    # Build advisors HTML
    advisors_html = ''
    for adv in advisors:
        advisors_html += f'''
        <div class="col-md-4 mb-4">
          <div class="card">
            <img class="card-img-top" src="/media/{adv['photo']}" alt="{adv['name']}">
            <div class="card-body">
              <h4 class="card-title">{adv['name']}</h4>
              <p class="card-text text-muted">
                <i class="fas fa-phone"></i> {adv['phone']}<br>
                <i class="fas fa-envelope"></i> {adv['email']}
              </p>
            </div>
          </div>
        </div>'''

    # MVP HTML
    mvp_html = ''
    if mvp:
        mvp_html = f'''
        <div class="card mb-3">
          <img class="card-img-top" src="/media/{mvp['photo']}" alt="{mvp['name']}">
          <div class="card-body">
            <h4 class="card-title text-center">{mvp['name']}</h4>
            <p class="card-text text-center text-success">
              <i class="fas fa-trophy"></i> Seller Of The Month
            </p>
            <p class="card-text text-center">
              <i class="fas fa-phone"></i> {mvp['phone']}
            </p>
          </div>
        </div>'''

    messages_html = _build_messages_html(request)
    is_auth = request.get('is_authenticated', False)
    user = request.get('user', {})

    html = render_template('about.html', {
        'advisors': advisors_html,
        'mvp': mvp_html,
        'messages': messages_html,
        'is_authenticated': 'true' if is_auth else '',
        'username': user.get('username', ''),
        'first_name': user.get('first_name', ''),
        'nav_home_active': '',
        'nav_about_active': 'active',
        'nav_listings_active': '',
    })

    return {'status': 200, 'body': html}


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
