"""
Carss Online Auto Dealer - Pure Python Web Server
No Django, No Flask - 100% Python
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
import urllib.parse
import os
import mimetypes
import json

from config import SERVER_HOST, SERVER_PORT, STATIC_DIR, MEDIA_DIR
from session import get_session_id_from_cookie, get_session
from handlers import pages, listings, accounts, contacts
from handlers import admin_panel


# URL Routes: (method, path) -> handler function
GET_ROUTES = {
    '/': pages.index,
    '/about': pages.about,
    '/listings': listings.index,
    '/listings/search': listings.search,
    '/accounts/login': accounts.login_page,
    '/accounts/register': accounts.register_page,
    '/accounts/logout': accounts.logout,
    '/accounts/dashboard': accounts.dashboard,
    # Admin
    '/admin': admin_panel.admin_login_page,
    '/admin/login': admin_panel.admin_login_page,
    '/admin/dashboard': admin_panel.admin_dashboard,
    '/admin/logout': admin_panel.admin_logout,
    '/admin/listings': admin_panel.admin_listings,
    '/admin/listings/add': admin_panel.admin_listing_add_page,
    '/admin/advisors': admin_panel.admin_advisors,
    '/admin/advisors/add': admin_panel.admin_advisor_add_page,
    '/admin/contacts': admin_panel.admin_contacts,
}

POST_ROUTES = {
    '/accounts/login': accounts.login_submit,
    '/accounts/register': accounts.register_submit,
    '/contacts/contact': contacts.contact_submit,
    # Admin
    '/admin/login': admin_panel.admin_login_submit,
    '/admin/listings/add': admin_panel.admin_listing_add_submit,
    '/admin/advisors/add': admin_panel.admin_advisor_add_submit,
}


class CarssHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path.rstrip('/')
        if path == '':
            path = '/'
        query_string = parsed.query
        params = urllib.parse.parse_qs(query_string)

        # Serve static files
        if path.startswith('/static/'):
            self.serve_static(path)
            return

        # Serve media files
        if path.startswith('/media/'):
            self.serve_media(path)
            return

        # Dynamic listing detail: /listings/<id>
        if path.startswith('/listings/') and path != '/listings/search':
            try:
                listing_id = int(path.split('/')[-1])
                self.handle_request(listings.detail, params, listing_id=listing_id)
                return
            except (ValueError, IndexError):
                pass

        # Admin dynamic routes: /admin/<section>/edit/<id>, /admin/<section>/delete/<id>
        import re
        admin_match = re.match(r'^/admin/(listings|advisors|contacts)/(edit|delete)/(\d+)$', path)
        if admin_match:
            section, action, item_id = admin_match.groups()
            handler_map = {
                ('listings', 'edit'): admin_panel.admin_listing_edit_page,
                ('listings', 'delete'): admin_panel.admin_listing_delete,
                ('advisors', 'edit'): admin_panel.admin_advisor_edit_page,
                ('advisors', 'delete'): admin_panel.admin_advisor_delete,
                ('contacts', 'delete'): admin_panel.admin_contact_delete,
            }
            func = handler_map.get((section, action))
            if func:
                self.handle_request(func, params, item_id=int(item_id))
                return

        # Route to handler
        handler_func = GET_ROUTES.get(path)
        if handler_func:
            self.handle_request(handler_func, params)
        else:
            self.send_error_page(404, 'Page Not Found')

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path.rstrip('/')

        # Parse form data
        content_type = self.headers.get('Content-Type', '')
        content_length = int(self.headers.get('Content-Length', 0))

        body = self.rfile.read(content_length).decode('utf-8')
        post_data = dict(urllib.parse.parse_qsl(body))

        # Admin dynamic POST routes: /admin/<section>/edit/<id>
        import re
        admin_match = re.match(r'^/admin/(listings|advisors)/(edit)/(\d+)$', path)
        if admin_match:
            section, action, item_id = admin_match.groups()
            handler_map = {
                ('listings', 'edit'): admin_panel.admin_listing_edit_submit,
                ('advisors', 'edit'): admin_panel.admin_advisor_edit_submit,
            }
            func = handler_map.get((section, action))
            if func:
                self.handle_request(func, post_data, item_id=int(item_id))
                return

        handler_func = POST_ROUTES.get(path)
        if handler_func:
            self.handle_request(handler_func, post_data)
        else:
            self.send_error_page(404, 'Page Not Found')

    def handle_request(self, handler_func, params, **kwargs):
        # Get session
        cookie_header = self.headers.get('Cookie', '')
        session_id = get_session_id_from_cookie(cookie_header)
        session = get_session(session_id) if session_id else None

        # Build request context
        request = {
            'params': params,
            'session_id': session_id,
            'session': session,
            'is_authenticated': session is not None and session.get('is_authenticated', False),
            'user': session if session else {},
            'handler': self,
        }
        request.update(kwargs)

        # Call handler
        response = handler_func(request)

        # Send response
        status = response.get('status', 200)
        headers = response.get('headers', {})
        body = response.get('body', '')
        redirect = response.get('redirect', None)

        if redirect:
            self.send_response(302)
            self.send_header('Location', redirect)
            for key, value in headers.items():
                self.send_header(key, value)
            self.end_headers()
        else:
            self.send_response(status)
            self.send_header('Content-Type', headers.get('Content-Type', 'text/html; charset=utf-8'))
            for key, value in headers.items():
                if key != 'Content-Type':
                    self.send_header(key, value)
            self.end_headers()
            if isinstance(body, str):
                self.wfile.write(body.encode('utf-8'))
            else:
                self.wfile.write(body)

    def serve_static(self, path):
        # /static/css/style.css -> STATIC_DIR/css/style.css
        rel_path = path[len('/static/'):]
        file_path = os.path.join(STATIC_DIR, rel_path.replace('/', os.sep))
        self.serve_file(file_path)

    def serve_media(self, path):
        # /media/photos/2020/03/25/car.jpg -> MEDIA_DIR/photos/2020/03/25/car.jpg
        rel_path = path[len('/media/'):]
        file_path = os.path.join(MEDIA_DIR, rel_path.replace('/', os.sep))
        self.serve_file(file_path)

    def serve_file(self, file_path):
        if os.path.isfile(file_path):
            mime_type, _ = mimetypes.guess_type(file_path)
            if mime_type is None:
                mime_type = 'application/octet-stream'
            self.send_response(200)
            self.send_header('Content-Type', mime_type)
            file_size = os.path.getsize(file_path)
            self.send_header('Content-Length', str(file_size))
            self.end_headers()
            with open(file_path, 'rb') as f:
                self.wfile.write(f.read())
        else:
            self.send_error_page(404, 'File Not Found')

    def send_error_page(self, code, message):
        self.send_response(code)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        html = f"""<!DOCTYPE html>
<html><head><title>{code} - {message}</title>
<link rel="stylesheet" href="/static/css/bootstrap.css"></head>
<body class="text-center" style="padding-top:100px;">
<h1>{code}</h1><p>{message}</p>
<a href="/" class="btn btn-primary">Go Home</a>
</body></html>"""
        self.wfile.write(html.encode('utf-8'))

    def log_message(self, format, *args):
        print(f"[{self.log_date_time_string()}] {args[0]}")


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in separate threads."""
    daemon_threads = True


def run():
    server = ThreadedHTTPServer((SERVER_HOST, SERVER_PORT), CarssHandler)
    print(f"""
============================================
  Carss Online Auto Dealer
  Pure Python Server (No Django/Flask)
============================================
  Running at: http://{SERVER_HOST}:{SERVER_PORT}/
  Press Ctrl+C to stop
============================================
""")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        server.server_close()


if __name__ == '__main__':
    run()
