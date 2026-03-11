# Setup Instructions for Team Members

## For Your Teammates

Follow these steps to get the project running locally:

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd ecommerce_platform
```

### Step 2: Set Up Python Environment

#### Windows
```bash
# Create virtual environment
python -m venv .venv

# Activate it
.venv\Scripts\activate

# Install dependencies
pip install -r backend/requirements.txt
```

####  macOS/Linux
```bash
# Create virtual environment
python3 -m venv .venv

# Activate it
source .venv/bin/activate

# Install dependencies
pip install -r backend/requirements.txt
```

###Step 3: Initialize Database

```bash
cd backend
python populate_db.py
cd ..
```

This creates sample products and users for testing.

### Step 4: Start Backend Server

```bash
cd backend
python app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
 * WARNING: This is a development server. Do not use it in production deployment.
```

### Step 5: Start Frontend Server (New Terminal)

```bash
# Method 1: Python HTTP Server
cd frontend
python -m http.server 8000

# Method 2: Node HTTP Server
npx http-server frontend -p 8000

# Method 3: VS Code Live Server (Install extension and right-click index.html)
```

### Step 6: Open in Browser

Visit: `http://localhost:8000`

## Testing the Application

### Login
1. Click "Account" navigation
2. Use these credentials:
   - Email: `john@example.com`
   - Password: `SecurePass@123`

###  Browse Products
1. Click "Products" to see all items
2. Use search functionality
3. Add items to cart or wishlist

### Test API
```bash
# Health check
curl http://localhost:5000/api/health

# Get products
curl http://localhost:5000/api/products?page=1

# Search
curl -X POST http://localhost:5000/api/search \
  -H "Content-Type: application/json" \
  -d '{"query": "headphones"}'
```

## Project Structure Overview

```
backend/           → Flask REST API
├── app.py        → Main application file
├── models/       → Database models (User, Product, Order, etc.)
└── routes/       → API endpoints

frontend/         → Vanilla JS + HTML + CSS
├── index.html    → Homepage with 3D chatbot
├── products.html → Product listing
├── cart.html     → Shopping cart
├── account.html  → User dashboard
├── js/           → JavaScript logic
└── css/          → Styling  
```

## Key Features to Test

- [ ] Browse products - works, fetches from backend
- [ ] Search products - search bar on every page
- [ ] Add to cart - click "Add to Basket" button
- [ ] Manage wishlist - click heart icons
- [ ] User authentication - login with sample accounts
- [ ] User profile - view and update account info
- [ ] Shopping cart calculations - subtotal, tax, shipping
- [ ] 3D Chatbot - floating button on homepage
- [ ] Mobile responsiveness - resize browser window

## Common Issues & Solutions

### Backend won't start
```bash
# Check if port 5000 is in use
netstat -ano | findstr :5000

# Kill the process (Windows)
taskkill /PID <PID> /F

# Or change the port in backend/app.py
```

### Products not loading
- Ensure backend is running (`python app.py`)
- Check browser console (F12) for errors
- Verify CORS is enabled (it is by default)

### Database errors
- Delete `backend/ecommerce.db`
- Re-run `python populate_db.py`
- Restart backend server

### CORS errors
- Make sure both backend and frontend are running
- Backend: `http://localhost:5000`
- Frontend: `http://localhost:8000`

## Environment Setup (.env)

Create `backend/.env` file (optional, has defaults):

```env
FLASK_ENV=development
SECRET_KEY=your-development-secret-key
JWT_SECRET_KEY=your-jwt-secret-key  
DATABASE_URL=sqlite:///ecommerce.db
```

## Next Steps

1. ✅ Setup complete!
2. 📚 Explore the codebase
3. 🔧 Test all features
4. 🐛 Report any bugs (GitHub Issues)
5. ✨ Propose improvements (Pull  Requests)

## Need Help?

- Check README_GITHUB.md for detailed documentation
- Review code comments in relevant files  
- Test using the sample data provided
- Open an issue with detailed description

## Git Workflow

```bash
# Create a feature branch
git checkout -b feature/your-feature

# Make changes and commit
git add .
git commit -m "Add your feature"

# Push and create PR
git push origin feature/your-feature
```

Good luck! 🚀
