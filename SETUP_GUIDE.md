# ShopHub E-Commerce Platform - Setup & Deployment Guide

## 🚀 Quick Start Guide

### 1. Frontend Setup

The frontend is ready to use immediately with no build process required!

#### Option A: Direct File Access
```bash
# Navigate to frontend folder
cd ecommerce_platform/frontend

# Open in your default browser
start index.html        # Windows
open index.html         # macOS
xdg-open index.html     # Linux
```

#### Option B: Local HTTP Server
```bash
# Using Python 3
cd ecommerce_platform/frontend
python -m http.server 8000

# Using Python 2
python -m SimpleHTTPServer 8000

# Visit: http://localhost:8000
```

#### Option C: Using Live Server
If you have Live Server extension:
```
Right-click on index.html → Open with Live Server
```

### 2. Backend Setup

#### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

#### Step-by-Step Installation

```bash
# 1. Navigate to backend directory
cd ecommerce_platform/backend

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Create .env file
# Windows (PowerShell):
echo "SECRET_KEY=dev-secret-key-change-in-production" > .env
echo "JWT_SECRET_KEY=jwt-secret-key-change-in-production" >> .env
echo "DATABASE_URL=sqlite:///ecommerce.db" >> .env

# macOS/Linux:
echo "SECRET_KEY=dev-secret-key-change-in-production" > .env
echo "JWT_SECRET_KEY=jwt-secret-key-change-in-production" >> .env
echo "DATABASE_URL=sqlite:///ecommerce.db" >> .env

# 6. Run the application
python app.py

# Server will start at: http://localhost:5000
```

## 🎯 Testing Features

### 1. Test Homepage
```
1. Visit http://localhost:8000 (or live server URL)
2. Scroll through featured products
3. See AI-curated recommendations
4. View trending deals
5. Check customer reviews
6. Notice security badges
```

### 2. Test Search Functionality
```
1. Click on search bar
2. Type "headphones" (note: typo tolerance works)
3. Try typing "hedphones" - should still find results
4. View search suggestions with categories
5. Search history is saved automatically
```

### 3. Test Product Catalog
```
1. Go to Products page
2. Use filters (Category, Price, Rating)
3. Sort by Price, Rating, or Date
4. Add products to cart
5. Check cart count updates
```

### 4. Test Shopping Cart
```
1. Add multiple products from homepage
2. Go to Cart page
3. Update quantities
4. See real-time price calculation (18% GST + ₹99 shipping)
5. Remove items
6. Click "Proceed to Checkout"
```

### 5. Test Accessibility Features
```
1. Press Tab key - navigate through all elements
2. Use keyboard shortcuts:
   - Alt + H: Go to Home
   - Alt + P: Go to Products
   - Alt + C: Go to Cart
   - Alt + S: Focus Search
3. Check Alt+Tab through site
4. Use screen reader (Narrator, NVDA, JAWS)
5. Click accessibility menu (♿) - bottom left:
   - Enable Color Blind Mode
   - Enable High Contrast
   - Adjust Text Size
6. Check Dark Mode (browser dark mode preference)
```

### 6. Test Authentication (Backend)
```bash
# Register
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123",
    "confirm_password": "password123"
  }'

# Login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'

# Response will include JWT token
```

### 7. Test Backend APIs
```bash
# Get all products
curl http://localhost:5000/api/products

# Search products
curl -X POST http://localhost:5000/api/products/search \
  -H "Content-Type: application/json" \
  -d '{"query": "headphones"}'

# Get recommendations (requires token)
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  http://localhost:5000/api/recommendations/personalized

# Get trending products
curl http://localhost:5000/api/recommendations/trending

# Health check
curl http://localhost:5000/api/health
```

## 📱 Testing on Mobile Devices

### Using Mobile Emulation
1. Open browser DevTools (F12 or Cmd+Option+I)
2. Click device toggle (or Ctrl+Shift+M)
3. Select iPhone or Android device
4. Test responsive design
5. Test touch interactions

### Local Network Access
```bash
# Find your computer's IP
# Windows: ipconfig (look for IPv4 Address)
# macOS/Linux: ifconfig (look for inet)

# Access from mobile on same network
http://YOUR_IP:8000
http://YOUR_IP:5000/api/health
```

## 🐛 Troubleshooting

### Frontend Issues

**Page not loading**
- Check if http.server is running
- Verify file paths are correct
- Clear browser cache (Ctrl+Shift+Del)
- Try incognito mode

**Styles not applying**
- Check browser console (F12)
- Verify CSS file paths
- Try hard refresh (Ctrl+Shift+R)

**Scripts not running**
- Open console and check for errors
- Verify app is initialized
- Check if localStorage is enabled

### Backend Issues

**Port 5000 already in use**
```bash
# Windows: Find and kill process
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS/Linux
lsof -ti:5000 | xargs kill -9
```

**ImportError for modules**
```bash
# Ensure virtual environment is activated
# Reinstall requirements
pip install --force-reinstall -r requirements.txt
```

**Database errors**
```bash
# Delete old database and recreate
rm ecommerce.db
python app.py
```

**CORS errors**
- This is expected if frontend and backend are on different ports
- CORS is configured to allow all origins in development
- Change `CORS_ORIGINS = ['*']` in config.py for production

## 🔒 Security Checklist

### Before Production Deployment
- [ ] Change SECRET_KEY to strong random value
- [ ] Change JWT_SECRET_KEY
- [ ] Set DEBUG = False
- [ ] Use PostgreSQL instead of SQLite
- [ ] Enable HTTPS/SSL
- [ ] Configure CORS properly
- [ ] Set secure cookie flags
- [ ] Implement rate limiting
- [ ] Set up logging
- [ ] Backup database regularly
- [ ] Use environment variables for secrets
- [ ] Enable CSRF protection
- [ ] Implement payment gateway (Razorpay, Stripe, etc.)
- [ ] Set up SSL certificates

## 📊 Database

### Initialize Database
```bash
cd backend
python app.py
# Database created automatically at first run
```

### View Database
```bash
# Using sqlite3 CLI
sqlite3 ecommerce.db

# Common queries:
# SELECT * FROM users;
# SELECT * FROM products;
# SELECT * FROM orders;
```

### Reset Database
```bash
rm ecommerce.db
python app.py
```

## 🚀 Deployment

### Heroku Deployment
```bash
# Install Heroku CLI and login
heroku create your-app-name

# Add Procfile
echo "web: gunicorn app:app" > backend/Procfile

# Deploy
git push heroku main

# Set environment variables
heroku config:set SECRET_KEY=your-secret
heroku config:set JWT_SECRET_KEY=your-jwt-secret
```

### Docker Deployment
```dockerfile
# Create Dockerfile in backend/
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

```bash
# Build and run
docker build -t shophub .
docker run -p 5000:5000 shophub
```

## 📈 Performance Optimization

### Frontend
- Enable gzip compression
- Minify CSS and JavaScript
- Use CDN for static files
- Implement service workers for offline
- Lazy load images

### Backend
- Add database indexes
- Cache frequently accessed data
- Use pagination for large datasets
- Implement connection pooling
- Use Redis for caching

## 📝 File Structure Reference

```
ecommerce_platform/
├── frontend/
│   ├── index.html              # Homepage
│   ├── products.html           # Product listing
│   ├── cart.html               # Shopping cart
│   ├── account.html            # User account
│   ├── css/
│   │   ├── styles.css
│   │   └── accessibility.css
│   ├── js/
│   │   ├── main.js
│   │   ├── search.js
│   │   ├── recommendations.js
│   │   └── accessibility.js
│   └── images/                 # Product images
│
└── backend/
    ├── app.py
    ├── config.py
    ├── requirements.txt
    ├── models/
    │   └── database.py
    ├── routes/
    │   ├── auth.py
    │   ├── products.py
    │   ├── orders.py
    │   ├── payments.py
    │   ├── users.py
    │   ├── recommendations.py
    │   └── search.py
    └── utils/
        ├── security.py
        └── validators.py
```

## 🎓 Learning Resources

### JavaScript Features Used
- ES6+ syntax
- Fetch API
- LocalStorage
- Regular expressions
- Levenshtein distance algorithm

### Python Features Used
- Flask framework
- SQLAlchemy ORM
- JWT authentication
- CORS handling
- Environment variables

### Accessibility Features
- ARIA labels
- Keyboard navigation
- Color contrast
- Screen reader support
- Semantic HTML

## 📞 Support

For issues or questions:
1. Check this guide
2. Review README.md
3. Check browser console (F12) for errors
4. Review backend logs
5. Create GitHub issue with:
   - Steps to reproduce
   - Error messages
   - Browser/OS information

## ✅ Verification Checklist

- [ ] Frontend loads without errors
- [ ] All pages are accessible
- [ ] Search works with typo tolerance
- [ ] Cart functionality works
- [ ] Backend API responds
- [ ] Database initializes
- [ ] Accessibility features work
- [ ] Mobile responsive layout works
- [ ] Dark mode works
- [ ] SSL badges visible

---

**Last Updated**: January 2026  
**Version**: 1.0.0
