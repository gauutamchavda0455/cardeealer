# Carss Online Auto Dealer - Project Explanation

## Project Overview
Carss Online Auto Dealer ek **car dealership website** hai jo **100% Pure Python** mein bani hai. Isme **koi bhi framework nahi** (No Django, No Flask) use kiya gaya hai. Sabkuch Python ke built-in modules se banaya gaya hai. Customers online cars browse kar sakte hain, search kar sakte hain, aur test drive request bhej sakte hain.

---

## Languages & Technologies Used

| Technology | Purpose | Version |
|-----------|---------|---------|
| **Python** | Backend programming language (100% Pure Python) | 3.12 |
| **MySQL (MariaDB)** | Database via XAMPP | 5.6+ |
| **HTML5** | Page structure / Markup | - |
| **CSS3** | Styling | - |
| **JavaScript** | Client-side interactivity | ES6 |
| **jQuery** | DOM manipulation & animations | 3.3.1 |
| **Bootstrap 4** | Responsive CSS framework | 4.x |
| **Font Awesome 5** | Icons library | 5.x |
| **Lightbox 2** | Image gallery viewer | 2.x |

**Total Languages: 4** (Python, HTML, CSS, JavaScript)
**Total Frameworks: 0** (No Django, No Flask - 100% Pure Python)
**Total Frontend Libraries: 4** (Bootstrap, jQuery, Font Awesome, Lightbox)

---

## Python Modules Used (Built-in + 1 External)

### Built-in Python Modules (Standard Library - No Install Required)
| Module | Purpose |
|--------|---------|
| `http.server` | HTTP web server |
| `socketserver.ThreadingMixIn` | Multi-threaded server (handles multiple requests) |
| `urllib.parse` | URL parsing, query string parsing |
| `os` | File path operations |
| `mimetypes` | MIME type detection for static files |
| `json` | JSON handling |
| `re` | Regular expressions (URL routing, template engine) |
| `uuid` | Unique session ID generation |
| `time` | Session expiry management |
| `hashlib` | SHA-256 session ID hashing |
| `http.cookies` | Cookie parsing (SimpleCookie) |
| `math` | Pagination calculations |

### External Library (Only 1 Install Required)
| Library | Purpose | Install Command |
|---------|---------|-----------------|
| `mysqlclient` (MySQLdb) | MySQL database connection & queries | `pip install mysqlclient` |

---

## Project Structure

```
carss_online_auto_dealer/
├── pure_python/                        # Main Pure Python Project
│   ├── app.py                          # HTTP Server + URL Routing (Entry Point)
│   ├── config.py                       # Server, Database, Path configuration
│   ├── db.py                           # MySQL database operations (raw SQL)
│   ├── session.py                      # Cookie-based session management
│   ├── template_engine.py              # Custom template engine ({{variable}}, {%include%})
│   │
│   ├── handlers/                       # Request Handlers (like Django views)
│   │   ├── __init__.py
│   │   ├── pages.py                    # Home & About page handlers
│   │   ├── listings.py                 # Car listings, detail, search handlers
│   │   ├── accounts.py                 # Login, Register, Dashboard handlers
│   │   ├── contacts.py                 # Test drive request handler
│   │   └── admin_panel.py              # Admin panel (CRUD operations)
│   │
│   ├── templates/                      # HTML Templates
│   │   ├── index.html                  # Home page
│   │   ├── about.html                  # About page
│   │   ├── listings.html               # All car listings
│   │   ├── listing_detail.html         # Single car detail
│   │   ├── search.html                 # Search results
│   │   ├── login.html                  # User login
│   │   ├── register.html               # User registration
│   │   ├── dashboard.html              # User dashboard
│   │   ├── partials/
│   │   │   ├── topbar.html             # Top bar (phone, email, social)
│   │   │   ├── navbar.html             # Navigation bar
│   │   │   └── footer.html             # Footer
│   │   └── admin/
│   │       ├── login.html              # Admin login
│   │       ├── dashboard.html          # Admin dashboard
│   │       ├── listings.html           # Admin listings list
│   │       ├── listing_form.html       # Admin add/edit listing
│   │       ├── advisors.html           # Admin advisors list
│   │       ├── advisor_form.html       # Admin add/edit advisor
│   │       └── contacts.html           # Admin contacts/inquiries
│   │
│   └── (uses carss/carss/static/ & carss/media/ for assets)
│
├── carss/                              # Old Django Project (reference only)
│   ├── carss/static/                   # CSS, JS, Images, Fonts
│   ├── media/                          # Uploaded car & advisor photos
│   └── ...
│
├── PROJECT_EXPLANATION.md              # This file
├── README.md
└── .gitignore
```

---

## Core Python Files - Kya Kaam Karta Hai

### 1. `app.py` - HTTP Server + URL Routing
- Python ka built-in `http.server.HTTPServer` use karta hai
- `ThreadingMixIn` se multi-threaded hai (multiple requests handle karta hai simultaneously)
- URL routing manually define ki hai (GET_ROUTES, POST_ROUTES dictionaries)
- Static files (`/static/`) aur media files (`/media/`) serve karta hai
- Dynamic routes handle karta hai (e.g., `/listings/5`, `/admin/listings/edit/3`)
- MIME type detection for CSS, JS, images, etc.

### 2. `config.py` - Configuration
- Server host & port settings
- MySQL database credentials
- File paths (static, media, templates)
- Session settings (secret key, cookie name, expiry time)
- Pagination settings

### 3. `db.py` - Database Layer (Raw SQL)
- `MySQLdb` library se direct MySQL connection
- 4 helper functions:
  - `fetch_all(sql, params)` - Multiple rows fetch karta hai (SELECT)
  - `fetch_one(sql, params)` - Single row fetch karta hai
  - `execute(sql, params)` - INSERT/UPDATE/DELETE operations
  - `count(sql, params)` - COUNT queries
- **No ORM** - saari queries raw SQL mein likhi hain
- Connection pooling: har request pe new connection, auto-close

### 4. `session.py` - Session Management
- In-memory session store (Python dictionary)
- SHA-256 hashed session IDs (uuid + secret key + timestamp)
- Cookie-based authentication (HttpOnly cookies)
- Flash messages system (success/error messages between requests)
- 24-hour session expiry
- Functions: create, get, delete session + cookie helpers

### 5. `template_engine.py` - Custom Template Engine
- `{{variable}}` syntax se variable substitution
- `{%include filename%}` se partial templates include
- Dynamic nav links (Login/Register ya Welcome/Logout based on auth)
- Helper functions: price formatting, HTML options builder, pagination HTML

---

## Request Handlers - Kya Kaam Karta Hai

### 1. Pages Handler (`handlers/pages.py`)
- **Home Page** (`GET /`) - Hero section with search form, 3 latest featured cars
- **About Page** (`GET /about`) - Company info, team members, Seller of the Month

### 2. Listings Handler (`handlers/listings.py`)
- **All Listings** (`GET /listings`) - Sabhi cars with pagination (6 per page)
- **Listing Detail** (`GET /listings/<id>`) - Car ki full detail, photos gallery, advisor info
- **Search** (`GET /listings/search`) - Cars search with 6 filters (condition, make, price, body style, fuel, transmission)

### 3. Accounts Handler (`handlers/accounts.py`)
- **Register Page** (`GET /accounts/register`) - Registration form
- **Register Submit** (`POST /accounts/register`) - User create (password hashing with SHA-256)
- **Login Page** (`GET /accounts/login`) - Login form
- **Login Submit** (`POST /accounts/login`) - Authentication + session create
- **Logout** (`GET /accounts/logout`) - Session destroy + cookie delete
- **Dashboard** (`GET /accounts/dashboard`) - User ke test drive requests

### 4. Contacts Handler (`handlers/contacts.py`)
- **Contact Submit** (`POST /contacts/contact`) - Test drive request save to database

### 5. Admin Panel Handler (`handlers/admin_panel.py`)
- **Admin Login** (`GET/POST /admin/login`) - Admin authentication
- **Admin Dashboard** (`GET /admin/dashboard`) - Stats overview (total cars, advisors, contacts)
- **Listings CRUD**:
  - `GET /admin/listings` - All listings list
  - `GET /admin/listings/add` - Add new listing form
  - `POST /admin/listings/add` - Save new listing
  - `GET /admin/listings/edit/<id>` - Edit listing form
  - `POST /admin/listings/edit/<id>` - Update listing
  - `GET /admin/listings/delete/<id>` - Delete listing
- **Advisors CRUD**:
  - `GET /admin/advisors` - All advisors list
  - `GET /admin/advisors/add` - Add new advisor form
  - `POST /admin/advisors/add` - Save new advisor
  - `GET /admin/advisors/edit/<id>` - Edit advisor form
  - `POST /admin/advisors/edit/<id>` - Update advisor
  - `GET /admin/advisors/delete/<id>` - Delete advisor
- **Contacts**:
  - `GET /admin/contacts` - View all test drive requests
  - `GET /admin/contacts/delete/<id>` - Delete contact

---

## Database Tables (MySQL)

### `auth_user` Table (Users)
```
- id            → User ID (auto-increment)
- username      → Username (unique)
- first_name    → First name
- last_name     → Last name
- email         → Email address
- password      → Hashed password (SHA-256)
- is_superuser  → Admin flag (1 = admin)
- is_active     → Active flag
- date_joined   → Registration date
```

### `advisors_advisor` Table (Sales Advisors)
```
- id            → Advisor ID (auto-increment)
- name          → Advisor ka naam
- photo         → Profile photo path
- description   → Bio/description
- phone         → Phone number
- email         → Email address
- is_mvp        → Seller of the Month flag (1/0)
- hire_date     → Joining date
```

### `listings_listing` Table (Cars)
```
- id            → Listing ID (auto-increment)
- advisor_id    → Assigned advisor (Foreign Key)
- vin           → Vehicle Identification Number
- condition     → New / Used
- body_style    → Sedan, SUV, Truck, etc.
- year          → Manufacturing year
- make          → Brand (Honda, Toyota, etc.)
- model         → Model name (Civic, Camry, etc.)
- price         → Car price
- color         → Exterior color
- interior_color → Interior color
- drivetrain    → AWD, FWD, RWD
- transmission  → Automatic / Manual
- fuel          → Diesel, Gasoline, Electric
- mileage       → Kilometers driven
- description   → Car description
- photo_main    → Main photo
- photo_1 to photo_4 → Additional photos (optional)
- is_published  → Show/hide on website (1/0)
- list_date     → Listing date
```

### `contacts_contact` Table (Test Drive Requests)
```
- id            → Contact ID (auto-increment)
- listing       → Car name
- listing_id    → Car ID
- name          → Customer name
- email         → Customer email
- phone         → Customer phone
- message       → Customer message
- contact_date  → Request date
- user_id       → Logged-in user ID
```

### Relationships
```
Advisor (1) ──── (Many) Listing
  └─ Ek advisor ke paas multiple cars ho sakti hain
  └─ Har car ek advisor ko assigned hoti hai

User (1) ──── (Many) Contact
  └─ Ek user multiple test drive requests bhej sakta hai
```

---

## Request-Response Flow (Kaise Kaam Karta Hai)

```
Browser Request
      │
      ▼
┌─────────────────────┐
│   app.py             │
│   (HTTP Server)      │
│   ThreadedHTTPServer │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│   URL Routing        │
│   GET_ROUTES /       │     ┌──────────────┐
│   POST_ROUTES        │────▶│ Static Files  │ (/static/*, /media/*)
│   Dynamic Routes     │     └──────────────┘
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐     ┌──────────────┐
│   Session Check      │────▶│ session.py    │
│   (Cookie parse)     │     │ (in-memory)   │
└──────┬──────────────┘     └──────────────┘
       │
       ▼
┌─────────────────────┐     ┌──────────────┐
│   Handler Function   │────▶│ db.py         │
│   (pages/listings/   │     │ (MySQL query) │
│    accounts/admin)   │     └──────────────┘
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐     ┌──────────────┐
│   Template Render    │────▶│ .html files   │
│   (template_engine)  │     │ (templates/)  │
└──────┬──────────────┘     └──────────────┘
       │
       ▼
   HTML Response
   (sent to browser)
```

---

## User Flow

### Visitor (Bina Login)
1. Home page pe aata hai → Featured cars dikhti hain
2. Search form se cars filter kar sakta hai (condition, make, price, etc.)
3. Car pe click kare → Full detail page dikhega (photos, specs, advisor info)
4. Featured Listings pe jaake saari cars dekh sakta hai

### Registered User
1. Register kare (Name, Username, Email, Password)
2. Login kare → Dashboard pe redirect hota hai
3. Dashboard pe apne saare test drive requests dikh jaate hain
4. Test drive form submit kar sakta hai

### Admin
1. `/admin` pe jaaye → Admin login page
2. Login kare → Admin dashboard (stats: total cars, advisors, contacts)
3. **Listings**: Add / Edit / Delete cars
4. **Advisors**: Add / Edit / Delete advisors (set MVP/Seller of Month)
5. **Contacts**: View / Delete test drive requests

---

## Django vs Pure Python - Kya Badla

| Feature | Django (Pehle) | Pure Python (Ab) |
|---------|---------------|-----------------|
| Web Server | Django dev server | `http.server.HTTPServer` + `ThreadingMixIn` |
| URL Routing | `urls.py` with `path()` | Dictionary-based routing in `app.py` |
| Database ORM | Django ORM (models.py) | Raw SQL queries via `MySQLdb` |
| Template Engine | Django Template Language | Custom `template_engine.py` ({{variable}}, {%include%}) |
| Session/Auth | Django sessions + auth | Custom `session.py` (in-memory + cookies) |
| Admin Panel | Django Admin (built-in) | Custom `admin_panel.py` (full CRUD) |
| Static Files | `collectstatic` command | Direct file serving with MIME detection |
| Forms | Django Forms | Raw HTML + POST data parsing |
| CSRF | Django CSRF middleware | Not needed (no framework middleware) |
| Password | PBKDF2 hashing | SHA-256 hashing |
| Dependencies | Django, Pillow, mysqlclient | Only mysqlclient |

---

## Database Setup
```
Database Engine: MySQL (MariaDB via XAMPP)
Database Name:   carssdb
User:            root
Password:        (empty)
Host:            localhost
Port:            3306
```

---

## Static & Media Files
- **Static Files** (`/static/`) → CSS, JS, Images, Fonts (Bootstrap, jQuery, Font Awesome)
- **Media Files** (`/media/`) → User-uploaded car photos & advisor photos
- Photos date-wise organized: `photos/YYYY/MM/DD/`
- Static files path: `carss/carss/static/`
- Media files path: `carss/media/`

---

## Key Features Summary
1. 100% Pure Python backend (No Django/Flask)
2. Multi-threaded HTTP server (handles concurrent requests)
3. Custom template engine with variable substitution & includes
4. Cookie-based session authentication
5. Car browsing with pagination (6 per page)
6. Advanced search with 6 filters (condition, make, price, body style, fuel, transmission)
7. Photo gallery with Lightbox viewer
8. User registration & login system
9. Test drive request form
10. Full Admin Panel with CRUD operations (Listings, Advisors, Contacts)
11. Flash messages (success/error notifications)
12. Responsive design (Bootstrap 4)
13. In-memory session management with 24-hour expiry

---

## How to Run

```bash
# 1. Start XAMPP (MySQL service must be running)

# 2. Create MySQL database 'carssdb' (if not exists)

# 3. Install only dependency
pip install mysqlclient

# 4. Go to pure_python folder
cd pure_python

# 5. Run server
python app.py

# 6. Open browser
# Website: http://127.0.0.1:8000/
# Admin:   http://127.0.0.1:8000/admin
```

---

## All URL Routes

| Method | URL | Handler | Description |
|--------|-----|---------|-------------|
| GET | `/` | pages.index | Home page |
| GET | `/about` | pages.about | About page |
| GET | `/listings` | listings.index | All car listings |
| GET | `/listings/<id>` | listings.detail | Car detail page |
| GET | `/listings/search` | listings.search | Search results |
| GET | `/accounts/login` | accounts.login_page | Login form |
| POST | `/accounts/login` | accounts.login_submit | Login submit |
| GET | `/accounts/register` | accounts.register_page | Register form |
| POST | `/accounts/register` | accounts.register_submit | Register submit |
| GET | `/accounts/logout` | accounts.logout | Logout |
| GET | `/accounts/dashboard` | accounts.dashboard | User dashboard |
| POST | `/contacts/contact` | contacts.contact_submit | Test drive request |
| GET | `/admin` | admin_panel.admin_login_page | Admin login |
| POST | `/admin/login` | admin_panel.admin_login_submit | Admin login submit |
| GET | `/admin/dashboard` | admin_panel.admin_dashboard | Admin dashboard |
| GET | `/admin/logout` | admin_panel.admin_logout | Admin logout |
| GET | `/admin/listings` | admin_panel.admin_listings | Admin listings |
| GET/POST | `/admin/listings/add` | admin_panel.admin_listing_add | Add listing |
| GET/POST | `/admin/listings/edit/<id>` | admin_panel.admin_listing_edit | Edit listing |
| GET | `/admin/listings/delete/<id>` | admin_panel.admin_listing_delete | Delete listing |
| GET | `/admin/advisors` | admin_panel.admin_advisors | Admin advisors |
| GET/POST | `/admin/advisors/add` | admin_panel.admin_advisor_add | Add advisor |
| GET/POST | `/admin/advisors/edit/<id>` | admin_panel.admin_advisor_edit | Edit advisor |
| GET | `/admin/advisors/delete/<id>` | admin_panel.admin_advisor_delete | Delete advisor |
| GET | `/admin/contacts` | admin_panel.admin_contacts | View contacts |
| GET | `/admin/contacts/delete/<id>` | admin_panel.admin_contact_delete | Delete contact |

---

*100% Pure Python - No Framework - Built with Python's standard library*
