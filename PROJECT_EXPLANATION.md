# Carss Online Auto Dealer - Project Explanation

## Project Overview
Carss Online Auto Dealer ek **car dealership website** hai jo **Django (Python)** framework pe bani hai. Isme customers online cars browse kar sakte hain, search kar sakte hain, aur test drive request bhej sakte hain.

---

## Languages & Technologies Used

| Technology | Purpose | Version |
|-----------|---------|---------|
| **Python** | Backend programming language | 3.7 |
| **Django** | Web framework | 4.2 |
| **MySQL** | Database | 5.6+ |
| **HTML5** | Page structure / Markup | - |
| **CSS3** | Styling | - |
| **JavaScript** | Client-side interactivity | ES6 |
| **jQuery** | DOM manipulation & animations | 3.3.1 |
| **Bootstrap 4** | Responsive CSS framework | 4.x |
| **Font Awesome 5** | Icons library | 5.x |
| **Lightbox 2** | Image gallery viewer | 2.x |
| **Pillow** | Image processing (photo uploads) | 10.0+ |

**Total Languages: 4** (Python, HTML, CSS, JavaScript)
**Total Frameworks/Libraries: 6** (Django, Bootstrap, jQuery, Font Awesome, Lightbox, Pillow)

---

## Project Structure

```
carss_online_auto_dealer/
├── carss/                          # Main Django project
│   ├── carss/                      # Project configuration
│   │   ├── settings.py             # Database, apps, middleware config
│   │   ├── urls.py                 # Main URL routing
│   │   ├── wsgi.py                 # WSGI entry point
│   │   └── asgi.py                 # ASGI entry point
│   │
│   ├── accounts/                   # User authentication app
│   ├── advisors/                   # Sales advisors app
│   ├── contacts/                   # Test drive requests app
│   ├── listings/                   # Car listings app
│   ├── pages/                      # Static pages app (Home, About)
│   │
│   ├── templates/                  # HTML templates
│   │   ├── base.html               # Master template
│   │   ├── accounts/               # Login, Register, Dashboard
│   │   ├── listings/               # Car listings & search
│   │   ├── pages/                  # Home & About pages
│   │   └── partials/               # Navbar, Footer, Alerts
│   │
│   ├── static/                     # CSS, JS, Images, Fonts
│   ├── media/                      # User-uploaded photos
│   ├── manage.py                   # Django management script
│   └── requirement.txt             # Python dependencies
│
├── screenshots/                    # Project screenshots
├── README.md
└── .gitignore
```

---

## 5 Django Apps - Kya Kaam Karta Hai Har App

### 1. Pages App (`pages/`)
- **Home Page** (`/`) - Hero section with search form, 3 latest featured cars, services section
- **About Page** (`/about`) - Company info, team members, Seller of the Month

### 2. Listings App (`listings/`)
- **All Listings** (`/listings/`) - Sabhi cars dikhata hai with pagination (6 per page)
- **Single Listing** (`/listings/<id>`) - Ek car ki full detail, photos gallery, advisor info, test drive form
- **Search** (`/listings/search`) - Cars search with filters (condition, make, price, body style, fuel, transmission)

### 3. Accounts App (`accounts/`)
- **Register** (`/accounts/register`) - New user registration
- **Login** (`/accounts/login`) - User login
- **Logout** (`/accounts/logout`) - User logout
- **Dashboard** (`/accounts/dashboard`) - User ke saare test drive requests dikhata hai

### 4. Advisors App (`advisors/`)
- Sales advisors/team members ka data manage karta hai
- Admin panel se advisors add/edit/delete kar sakte hain
- "Seller of the Month" (MVP) feature

### 5. Contacts App (`contacts/`)
- Test drive request form handle karta hai
- Duplicate request check karta hai (same user same car ke liye dobara request nahi de sakta)
- Automated confirmation email bhejta hai

---

## Database Models (Tables)

### Advisor Model
```
- name          → Advisor ka naam
- photo         → Profile photo
- description   → Bio/description
- phone         → Phone number
- email         → Email address
- is_mvp        → Seller of the Month flag (True/False)
- hire_date     → Joining date
```

### Listing Model (Car)
```
- advisor       → Assigned advisor (ForeignKey)
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
- is_published  → Show/hide on website
```

### Contact Model (Test Drive Request)
```
- listing       → Car name
- listing_id    → Car ID
- name          → Customer name
- email         → Customer email
- phone         → Customer phone
- message       → Customer message
- contact_date  → Request date
- user_id       → Logged-in user ID (optional)
```

### Relationships
```
Advisor (1) ──── (Many) Listing
  ↑
  └─ Ek advisor ke paas multiple cars ho sakti hain
  └─ Har car ek advisor ko assigned hoti hai
```

---

## Kaise Kaam Karta Hai - User Flow

### Visitor (Bina Login)
1. Home page pe aata hai → Featured cars dikhti hain
2. Search form se cars filter kar sakta hai (condition, make, price, etc.)
3. Car pe click kare → Full detail page dikhega (photos, specs, advisor info)
4. "Schedule A Test Drive" button → Modal form open hota hai
5. Form fill karke submit → Confirmation email aata hai

### Registered User
1. Register kare (Name, Username, Email, Password)
2. Login kare → Dashboard pe redirect hota hai
3. Dashboard pe apne saare test drive requests dikh jaate hain
4. Test drive form mein name/email auto-fill hota hai
5. Same car ke liye dobara request nahi de sakta (duplicate check)

### Admin
1. `/admin/` pe jaaye → Django admin panel
2. Cars add/edit/delete kar sakta hai
3. Advisors manage kar sakta hai
4. Test drive requests dekh sakta hai
5. "Seller of the Month" set kar sakta hai

---

## Database Setup
```python
Database: MySQL
Name:     carssdb
User:     root
Password: (empty)
Host:     localhost
Port:     3306
```

---

## Email Integration
- Test drive request submit hone pe automated email jaata hai
- Django ka built-in `send_mail` function use hota hai
- Email sender: `wandev.projects@gmail.com`

---

## Static & Media Files
- **Static Files** (`/static/`) → CSS, JS, Images, Fonts (Bootstrap, jQuery, Font Awesome)
- **Media Files** (`/media/`) → User-uploaded car photos & advisor photos
- Photos date-wise organized hoti hain: `photos/YYYY/MM/DD/`

---

## Key Features Summary
1. Car browsing with pagination
2. Advanced search with 6 filters
3. Photo gallery with Lightbox viewer
4. User registration & login system
5. Test drive request with duplicate prevention
6. Automated email notifications
7. Sales advisor management with MVP feature
8. Responsive design (Bootstrap 4)
9. Customized Django admin panel
10. Session-based authentication with CSRF protection

---

## How to Run
```bash
# 1. Install dependencies
pip install -r requirement.txt

# 2. Setup MySQL database 'carssdb'

# 3. Run migrations
python manage.py migrate

# 4. Create superuser
python manage.py createsuperuser

# 5. Run server
python manage.py runserver
```

---

*Generated for project documentation purposes.*
