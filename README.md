# 🛍️ ShopHub — Full-Stack E-Commerce Platform

<div align="center">

![Flask](https://img.shields.io/badge/Flask-2.3.0-green?style=for-the-badge&logo=flask)
![JavaScript](https://img.shields.io/badge/JavaScript-Vanilla-yellow?style=for-the-badge&logo=javascript)
![SQLite](https://img.shields.io/badge/Database-SQLite-blue?style=for-the-badge&logo=sqlite)
![License](https://img.shields.io/badge/License-MIT-red?style=for-the-badge)

**A modern, full-stack e-commerce platform built with Flask backend and Vanilla JavaScript frontend.**

[Features](#-features) • [Tech Stack](#-tech-stack) • [Quick Start](#-quick-start) • [API Docs](#-api-endpoints) • [Team Setup](#-for-teammates)

</div>

---

## 📌 Overview

**ShopHub** is a production-ready e-commerce platform demonstrating professional full-stack web development. It includes a RESTful Flask API backend with JWT authentication, a dynamic Vanilla JS frontend, SQLite database with 8 relational models, and a complete shopping experience with cart, wishlist, search, and recommendations.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🔐 **User Authentication** | JWT-based login, registration, and profile management |
| 🛒 **Shopping Cart** | Add/remove items, auto-calculated subtotal, tax and shipping |
| ❤️ **Wishlist** | Save favorites, sync with backend, persistent storage |
| 🔍 **Smart Search** | Typo-tolerant search with live suggestions |
| 🤖 **Recommendations** | Personalized product suggestions based on purchase history |
| 💰 **Loyalty Program** | Bronze to Silver to Gold to Platinum tier system |
| 📱 **Responsive Design** | Mobile-first layout for all screen sizes |
| ♿ **Accessibility** | WCAG 2.1 compliant with keyboard navigation |
| 💬 **3D Chatbot** | Interactive CSS chatbot widget on homepage |
| 📦 **Order Management** | Create, track, and manage orders |

---

## 🏗️ Tech Stack

### Backend
- **Flask 2.3.0** — Python web framework
- **SQLAlchemy** — ORM for database models
- **Flask-JWT-Extended** — JWT authentication
- **Flask-CORS** — Cross-origin resource sharing
- **SQLite** — Lightweight database

### Frontend
- **Vanilla JavaScript** — No frameworks, pure JS
- **HTML5 + CSS3** — Semantic markup and modern styling
- **Local Storage** — Offline-capable cart/wishlist

---

## 📁 Project Structure

```
ecommerce_platform/
│
├── 📂 backend/
│   ├── app.py                  # Flask app entry point
│   ├── config.py               # App configuration
│   ├── requirements.txt        # Python dependencies
│   ├── populate_db.py          # Initialize database with sample data
│   ├── sample_data.py          # Sample products and users
│   ├── .env.example            # Environment variables template
│   ├── 📂 models/
│   │   └── database.py         # SQLAlchemy models
│   └── 📂 routes/
│       ├── auth.py             # Login, Register, Profile
│       ├── products.py         # Product catalog
│       ├── orders.py           # Order management
│       ├── payments.py         # Payment processing
│       ├── wishlist.py         # Wishlist CRUD
│       ├── search.py           # Search and suggestions
│       ├── recommendations.py  # Personalized picks
│       └── users.py            # Loyalty and user info
│
├── 📂 frontend/
│   ├── index.html              # Homepage + 3D chatbot
│   ├── products.html           # Product catalog page
│   ├── cart.html               # Shopping cart
│   ├── account.html            # User dashboard
│   ├── 📂 css/
│   │   ├── styles.css          # Main stylesheet
│   │   └── accessibility.css   # A11y styles
│   └── 📂 js/
│       ├── main.js             # Core app logic + API calls
│       ├── search.js           # Search functionality
│       ├── wishlist.js         # Wishlist management
│       ├── recommendations.js  # Product recommendations
│       └── accessibility.js    # Accessibility features
│
├── .gitignore
└── README.md
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/PrateekAgrawal2005/Coder-s-Fest.git
cd Coder-s-Fest
```

### 2. Set Up Python Environment

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r backend/requirements.txt
```

### 4. Initialize Database

```bash
cd backend
python populate_db.py
```

This creates **15 sample products** and **3 test users** automatically.

### 5. Start Backend Server

```bash
python app.py
```

API running at `http://localhost:5000`

### 6. Start Frontend (New Terminal)

```bash
cd frontend
python -m http.server 8000
```

Website at `http://localhost:8000`

---

## 🔑 Test Accounts

| Username | Email | Password |
|----------|-------|----------|
| john_doe | john@example.com | SecurePass@123 |
| jane_smith | jane@example.com | SecurePass@456 |
| demo_user | demo@shopHub.com | Demo@12345 |

---

## 📡 API Endpoints

### Authentication
```
POST   /api/auth/register      Register new user
POST   /api/auth/login         Login and get JWT token
GET    /api/auth/profile       Get current user profile
PUT    /api/auth/profile       Update profile
```

### Products
```
GET    /api/products           Get all products (paginated)
GET    /api/products/<id>      Get single product
GET    /api/search?q=<query>   Search products
GET    /api/search/suggestions Search suggestions
```

### Wishlist (JWT required)
```
GET    /api/wishlist                      Get user wishlist
POST   /api/wishlist                      Add item to wishlist
DELETE /api/wishlist/<id>                 Remove by wishlist ID
DELETE /api/wishlist/product/<id>         Remove by product ID
DELETE /api/wishlist/clear                Clear entire wishlist
GET    /api/wishlist/check/<id>           Check if product is wishlisted
```

### Orders (JWT required)
```
GET    /api/orders             Get user orders
GET    /api/orders/<id>        Get order details
POST   /api/orders             Create new order
```

### Other
```
POST   /api/payments/initialize              Initialize payment
GET    /api/recommendations/personalized     Personalized picks
GET    /api/users/loyalty-info               Loyalty info
GET    /api/health                           Health check
```

---

## 🧪 Testing the API

```bash
# Health check
curl http://localhost:5000/api/health

# Get all products
curl http://localhost:5000/api/products?page=1

# Search products
curl -X POST http://localhost:5000/api/search \
  -H "Content-Type: application/json" \
  -d "{\"query\": \"headphones\"}"

# Login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d "{\"email\": \"john@example.com\", \"password\": \"SecurePass@123\"}"
```

---

## 👥 For Teammates

### Contributing Workflow

```bash
# 1. Get latest code
git pull origin master

# 2. Create your feature branch
git checkout -b feature/your-feature-name

# 3. Make changes and commit
git add .
git commit -m "Add: your feature description"

# 4. Push and open Pull Request
git push origin feature/your-feature-name
```

### Branch Naming Convention
- `feature/` — New features
- `fix/` — Bug fixes
- `docs/` — Documentation updates
- `style/` — CSS/UI changes

---

## 🗄️ Database Models

| Model | Description |
|-------|-------------|
| User | User accounts, profiles, loyalty info |
| Product | Product catalog with pricing and inventory |
| Order | Customer orders with status tracking |
| OrderItem | Individual items within an order |
| Review | Product reviews and ratings |
| Payment | Payment records and status |
| Wishlist | User saved products |

---

## ⚙️ Environment Configuration

Copy `backend/.env.example` to `backend/.env` and update values:

```env
FLASK_ENV=development
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
DATABASE_URL=sqlite:///ecommerce.db
```

---

## 🔒 Security Features

- JWT token authentication with 30-day expiry
- Password hashing with Werkzeug
- CORS configured for secure cross-origin requests
- Input validation on all API endpoints
- SQL injection protection via SQLAlchemy ORM
- Authorization checks on all protected routes

---

## 📊 Project Stats

- **51 files** tracked in Git
- **20+ API endpoints** across 8 route modules
- **8 database models** with full relational integrity
- **4 HTML pages** with responsive design
- **15 sample products** across 4 categories
- **3 pre-built test accounts**

---

## 🤝 Team Members

Built by the **Coder''s Fest** team.

---

## 📄 License

This project is licensed under the **MIT License**.

---

<div align="center">

**Star this repo if you found it helpful!**

[View Live Repo](https://github.com/PrateekAgrawal2005/Coder-s-Fest)

</div>
