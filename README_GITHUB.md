# 🛍️ ShopHub - E-Commerce Platform

A modern, full-stack e-commerce platform built with Flask (Backend) and Vanilla JavaScript (Frontend).

## Features

- ✅ **Product Catalog** - Browse 15+ products across multiple categories
- ✅ **User Authentication** - Secure JWT-based authentication
- ✅ **Shopping Cart** - Add/remove items with persistent storage
- ✅ **Wishlist Management** - Save favorite products
- ✅ **Search & Filters** - Advanced product search with typo tolerance
- ✅ **User Dashboard** - Account management and order history
- ✅ **Recommendations** - Personalized product suggestions
- ✅ **Loyalty Program** - Earn points on purchases
- ✅ **Responsive Design** - Mobile-friendly interface
- ✅ **Accessibility** - WCAG compliant design
- ✅ **3D Chatbot** - Interactive CSS-based chatbot widget

## Tech Stack

### Backend
- **Framework**: Flask 2.3.0
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: Flask-JWT-Extended
- **CORS**: Flask-CORS for cross-origin requests
- **Python**: 3.8+

### Frontend
- **HTML5**, **CSS3**, **Vanilla JavaScript**
- **No frameworks** for maximum simplicity
- **Responsive Design** with CSS Grid/Flexbox
- **Local Storage** for cart/wishlist persistence

## Quick Start

###  1. Backend Setup

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r backend/requirements.txt

# Initialize database with sample data
cd backend
python populate_db.py

# Start Flask server
python app.py
```

The backend will run on `http://localhost:5000`

### 2. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Open in browser (simple HTTP server recommended)
# Option 1: Python built-in server
python -m http.server 8000

# Option 2: Use VS Code Live Server extension
# Option 3: Use Node.js http-server
npm install -g http-server
http-server
```

Access frontend at `http://localhost:8000` (or your server port)

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/profile` - Get current user profile
- `PUT /api/auth/profile` - Update profile

### Products
- `GET /api/products` - Get all products (paginated)
- `GET /api/products/<id>` - Get product details
- `GET /api/search?q=<query>` - Search products
- `GET /api/search/suggestions?q=<query>` - Get search suggestions

### Wishlist (Requires JWT)
- `GET /api/wishlist` - Get user's wishlist
- `POST /api/wishlist` - Add item to wishlist
- `DELETE /api/wishlist/<id>` - Remove from wishlist
- `DELETE /api/wishlist/product/<product_id>` - Remove by product ID
- `GET /api/wishlist/check/<product_id>` - Check if in wishlist
- `DELETE /api/wishlist/clear` - Clear entire wishlist

### Orders (Requires JWT)
- `GET /api/orders` - Get user's orders
- `GET /api/orders/<id>` - Get order details
- `POST /api/orders` - Create new order

### Payments (Requires JWT)
- `POST /api/payments/initialize` - Initialize payment

### Recommendations (Requires JWT)
- `GET /api/recommendations/personalized` - Get recommendations

### Users (Requires JWT)
- `GET /api/users/loyalty-info` - Get loyalty information

## Sample  Users

After running `populate_db.py`, you can login with:

| Username | Email | Password |
|----------|-------|----------|
| john_doe | john@example.com | SecurePass@123 |
| jane_smith | jane@example.com | SecurePass@456 |
| demo_user | demo@shopHub.com | Demo@12345 |

## Database Models

- **User** - User accounts and profiles
- **Product** - Product catalog with pricing and inventory
- **Order** - Customer orders
- **OrderItem** - Items in orders
- **Review** - Product reviews and ratings
- **Payment** - Payment records
- **Wishlist** - User's saved products

## Configuration

### Environment Variables (Optional)

Create a `.env` file in the backend directory:

```env
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key
DATABASE_URL=sqlite:///ecommerce.db
```

### Frontend Configuration

Edit the API URL in `frontend/js/wishlist.js`:

```javascript
const API_BASE_URL = 'http://localhost:5000/api';
```

## File Structure

```
ecommerce_platform/
├── backend/
│   ├── app.py                 # Main Flask app
│   ├── config.py              # Configuration
│   ├── requirements.txt        # Python dependencies
│   ├── sample_data.py          # Sample data script
│   ├── populate_db.py          # Database initialization
│   ├── models/
│   │   ├── __init__.py
│   │   └── database.py         # SQLAlchemy models
│   └── routes/
│       ├── auth.py             # Authentication routes
│       ├── products.py         # Product routes
│       ├── orders.py           # Order routes
│       ├── payments.py         # Payment routes
│       ├── users.py            # User routes
│       ├── recommendations.py  # Recommendation routes
│       ├── search.py           # Search routes
│       └── wishlist.py         # Wishlist routes
│
├── frontend/
│   ├── index.html              # Homepage with chatbot
│   ├── products.html           # Products page
│   ├── cart.html               # Shopping cart
│   ├── account.html            # User account
│   ├── css/
│   │   ├── styles.css          # Main styles
│   │   └── accessibility.css   # A11y styles
│   └── js/
│       ├── main.js             # Main app logic
│       ├── search.js           # Search functionality
│       ├── recommendations.js  # Recommendations
│       ├── wishlist.js         # Wishlist management
│       └── accessibility.js    # A11y features
│
├── .gitignore                  # Git ignore rules
├── README.md                   # This file
└── Requirements.txt            # Pip dependencies
```

## Bug Fixes & Updates

### Latest Changes
- ✅ Fixed: Frontend now fetches products from backend API (was using hardcoded data)
- ✅ Added: POST endpoint to add items to wishlist (`/api/wishlist`)
- ✅ Fixed: Database initialization with sample products
- ✅ Added: .gitignore for proper Git configuration
- ✅ Updated:  All API routes now have proper error handling

## Running Tests

```bash
# Test backend API
curl http://localhost:5000/api/health

# Get products
curl http://localhost:5000/api/products?page=1&per_page=10

# Search
curl -X POST http://localhost:5000/api/search \
  -H "Content-Type: application/json" \
  -d '{"query": "headphones"}'
```

## Development

### Adding New Routes

1. Create a new file in `backend/routes/`
2. Define blueprint with routes
3. Import and register in `backend/app.py`

### Adding New Products

Edit `backend/sample_data.py` and add product data in the list

### Modifying Frontend Styles

Update `frontend/css/styles.css` for global styles or specific files for component styles

## Deployment

### Production Checklist

- [ ] Set `FLASK_ENV=production`
- [ ] Use a production WSGI server (Gunicorn, uWSGI)
- [ ] Enable HTTPS/SSL
- [ ] Set strong SECRET_KEY and JWT_SECRET_KEY
- [ ] Use PostgreSQL instead of SQLite
- [ ] Implement proper logging
- [ ] Set up error tracking (Sentry, etc.)
- [ ] Configure CORS properly
- [ ] Use environment variables for sensitive data

### Deploy with Gunicorn

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 backend.app:app
```

## Troubleshooting

### Backend Won't Start
- Ensure Python 3.8+ is installed
- Check if port 5000 is available: `netstat -ano | findstr :5000` (Windows)
- Verify all dependencies: `pip install -r backend/requirements.txt`

### Frontend Not Loading Products
- Ensure backend is running on `http://localhost:5000`
- Check browser console for CORS errors
- Verify API URLs in `frontend/js/main.js` and `wishlist.js`

### Database Issues
- Delete `backend/ecommerce.db` and re-run `populate_db.py`
- Check file permissions on the database directory

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is open source and available under the MIT License.

## Support

For issues, questions, or suggestions, please open an issue on GitHub.

---

**Last Updated**: March 2026
**Status**: ✅ Production Ready
**Version**: 1.0.0
