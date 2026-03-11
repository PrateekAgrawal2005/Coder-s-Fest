# Testing & QA Guide

## Manual Testing Checklist

### Backend Testing

#### 1. Server Health
```bash
# Test: Server is running
curl http://localhost:5000/api/health

# Expected: 200 OK
```

#### 2. Product Management
```bash
# Get all products
curl http://localhost:5000/api/products?page=1&per_page=10

# Get single product
curl http://localhost:5000/api/products/{product_id}

# Search products
curl -X POST http://localhost:5000/api/search \
  -H "Content-Type: application/json" \
  -d '{"query": "headphones"}'

# Get search suggestions
curl http://localhost:5000/api/search/suggestions?q=phone
```

#### 3. Authentication
```bash
# Register new user
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "TestPass@123",
    "confirm_password": "TestPass@123"
  }'

# Login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "SecurePass@123"
  }'

# Get JWT token from response and use in next requests with:
# Authorization: Bearer {token}
```

#### 4. Wishlist (Requires Authentication)
```bash
# Get wishlist
curl http://localhost:5000/api/wishlist \
  -H "Authorization: Bearer {YOUR_JWT_TOKEN}"

# Add to wishlist
curl -X POST http://localhost:5000/api/wishlist \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {YOUR_JWT_TOKEN}" \
  -d '{"product_id": "{product_id}"}'

# Remove from wishlist
curl -X DELETE http://localhost:5000/api/wishlist/{product_id} \
  -H "Authorization: Bearer {YOUR_JWT_TOKEN}"

# Clear wishlist
curl -X DELETE http://localhost:5000/api/wishlist/clear \
  -H "Authorization: Bearer {YOUR_JWT_TOKEN}"
```

### Frontend Testing

#### 1. Basic Navigation
- [ ] Homepage loads without errors
- [ ] Navigation menu items are clickable
- [ ] Mobile menu toggle works (resize browser to < 768px)
- [ ] All pages load correctly

#### 2. Product Browsing
- [ ] Products page displays all products
- [ ] Product cards show correct information
- [ ] Images/emojis display properly
- [ ] Price and discount are calculated correctly
- [ ] Stock status is accurate

#### 3. Search Functionality
- [ ] Search input is functional
- [ ] Search suggestions appear when typing
- [ ] Search results are filtered correctly
- [ ] Empty search shows error message

#### 4. Shopping Cart
- [ ] Can add products to cart
- [ ] Cart count badge updates
- [ ] Cart page shows all items
- [ ] Quantity can be changed
- [ ] Items can be removed with confirmation
- [ ] Total calculations are correct (subtotal + tax + shipping)
- [ ] Empty cart message shows when no items

#### 5. Wishlist
- [ ] Can add products to wishlist
- [ ] Wishlist count updates
- [ ] Wishlist items persist after page reload
- [ ] Can remove items from wishlist
- [ ] Heart icon shows saved status
- [ ] Account page displays wishlist

#### 6. User Account
- [ ] Can log in with sample credentials
- [ ] Can view profile information
- [ ] Can update profile details
- [ ] Can view order history
- [ ] Can view loyalty information
- [ ] Can log out

#### 7. Chatbot
- [ ] Floating chat button is visible
- [ ] Click opens chat window
- [ ] Can type messages
- [ ] Gets automated responses
- [ ] Can close chat window
- [ ] Works on mobile

#### 8. Responsive Design
- [ ] Desktop view (> 1200px) works
- [ ] Tablet view (768px - 1200px) works
- [ ] Mobile view (< 768px) works
- [ ] All text is readable
- [ ] Buttons are clickable on all sizes
- [ ] No horizontal scrolling on mobile

#### 9. Accessibility
- [ ] Can navigate with keyboard (Tab key)
- [ ] Can skip to main content
- [ ] Color contrast is sufficient
- [ ] Form labels are associated with inputs
- [ ] Images have alt text
- [ ] Links have descriptive text

### Sample Test Data

#### Test Accounts
```
Account 1:
- Email: john@example.com
- Password: SecurePass@123
- Orders: Yes

Account 2:
- Email: jane@example.com  
- Password: SecurePass@456
- Orders: Yes

Account 3:
- Email: demo@shopHub.com
- Password: Demo@12345
- Orders: No
```

#### Test Products
- 15 products across 4 categories
- Electronics, Fashion, Groceries, Lifestyle
- Prices range from ₹199 to ₹94,999
- All have stock levels > 0

### Performance Testing

```bash
# Time to load homepage (should be < 2s)
curl -w "@curl-format.txt" -o /dev/null -s http://localhost:8000

# Test API response time
curl -w "Response time: %{time_total}s\n" -o /dev/null -s http://localhost:5000/api/products

# Expected API response: < 100ms
# Expected page load: < 2s
```

### Error Scenarios to Test

#### Backend Errors
- [ ] Invalid JWT token returns 401
- [ ] Missing required fields return 400
- [ ] Non-existent product returns 404
- [ ] Database errors return 500 with proper message

#### Frontend Errors
- [ ] Backend offline shows fallback demo data
- [ ] Network error shows notification
- [ ] Form validation prevents invalid submission
- [ ] Missing cart item handles gracefully

### Browser Compatibility

- [ ] Chrome
- [ ] Firefox
- [ ] Safari
- [ ] Edge
- [ ] Mobile Safari (iOS)
- [ ] Chrome Mobile (Android)

### Security Checklist

- [ ] No sensitive data in localStorage (except cart)
- [ ] JWT tokens properly sent in requests
- [ ] CORS is properly configured
- [ ] No SQL injection vulnerabilities
- [ ] No XSS vulnerabilities in user inputs
- [ ] Passwords are hashed in database

## Automated Testing (Optional)

### Backend Unit Tests
```bash
# Create tests/test_api.py with pytest
pip install pytest
pytest tests/
```

### Frontend Tests
```bash
# Install test framework
npm install --save-dev jest

# Run tests
npm test
```

## Load Testing

```bash
# Install Apache Bench
# Windows: https://httpd.apache.org/download.cgi

# Test API endpoint
ab -n 1000 -c 10 http://localhost:5000/api/products

# Expected: Handle 1000 requests with 10 concurrent connections
```

## Issue Reporting Template

When reporting bugs, include:

```markdown
## Bug Report

**Title**: [Brief description of issue]

**Environment**:
- Browser: [Chrome/Firefox/etc] Version: [X.X]
- OS: [Windows/Mac/Linux]
- Backend: Running/Not running

**Steps to Reproduce**:
1. Step 1
2. Step 2
3. Step 3

**Expected Behavior**:
[What should happen]

**Actual Behavior**:
[What actually happens]

**Screenshots**:
[If applicable]

**Console Errors**:
[Copy from browser F12]
```

## Performance Optimization Checklist

- [ ] Images are optimized
- [ ] CSS is minified in production
- [ ] JS is minified in production
- [ ] Database queries are optimized
- [ ] No N+1 query problems
- [ ] Caching is implemented
- [ ] API responses are paginated
```

---

**Last Updated**: March 2026
