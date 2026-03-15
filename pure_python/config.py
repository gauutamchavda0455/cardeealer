import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Server
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 8000

# Database (MySQL via XAMPP)
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'carssdb',
    'port': 3306,
}

# Paths - use Django's existing static and media folders
DJANGO_DIR = os.path.join(os.path.dirname(BASE_DIR), 'carss')
STATIC_DIR = os.path.join(DJANGO_DIR, 'carss', 'static')
MEDIA_DIR = os.path.join(DJANGO_DIR, 'media')
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')

# Session
SECRET_KEY = 'carss-pure-python-secret-key-change-in-production'
SESSION_COOKIE_NAME = 'session_id'
SESSION_EXPIRY = 86400  # 24 hours in seconds

# Pagination
LISTINGS_PER_PAGE = 6
