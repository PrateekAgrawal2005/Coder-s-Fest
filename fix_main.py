#!/usr/bin/env python3
"""
Fix the main.js to fetch products from backend API instead of hardcoded data
"""

# Read the file
with open('frontend/js/main.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the loadProducts function and replace it
new_load_products = '''    loadProducts() {
        // Fetch products from backend API
        const API_URL = 'http://localhost:5000/api';
        
        fetch(`${API_URL}/products?page=1&per_page=50`)
            .then(response => response.json())
            .then(data => {
                // Convert backend products to frontend format
                this.products = data.products.map(p => ({
                    id: p.id,
                    name: p.name,
                    category: p.category,
                    price: p.price,
                    original_price: p.original_price,
                    rating: p.average_rating || 4.5,
                    reviews: p.total_reviews || 0,
                    image: '📦',  // Default emoji
                    inStock: p.stock > 0,
                    stock: p.stock,
                    discount: p.discount_percentage,
                    description: p.description || '',
                    specs: []
                }));
                
                // Re-render sections with loaded data
                this.renderFeaturedProducts();
                this.renderTrendingDeals();
                this.renderExpertPicks();
            })
            .catch(error => {
                console.error('Error loading products:', error);
                // Fall back to demo data if API fails
                this.loadDemoProducts();
            });
    }
    
    loadDemoProducts() {
        // Fallback demo data if API is not available
        this.products = [
            {
                id: '1',
                name: 'Sony WH-1000XM5 Headphones',
                category: 'Electronics',
                price: 18999,
                original_price: 29999,
                rating: 4.8,
                reviews: 2450,
                image: '🎧',
                inStock: true,
                stock: 45,
                discount: 37,
                description: 'Industry-leading noise cancellation with 30-hour battery life',
                specs: []
            },
            {
                id: '2',
                name: 'Apple Watch Series 8',
                category: 'Electronics',
                price: 34999,
                original_price: 41999,
                rating: 4.6,
                reviews: 5200,
                image: '⌚',
                inStock: true,
                stock: 28,
                discount: 17,
                description: 'Advanced health monitoring and fitness tracking',
                specs: []
            },
            {
                id: '3',
                name: 'Premium Cotton T-Shirt',
                category: 'Fashion',
                price: 799,
                original_price: 1799,
                rating: 4.5,
                reviews: 1856,
                image: '👕',
                inStock: true,
                stock: 120,
                discount: 55,
                description: 'Comfortable organic cotton everyday wear',
                specs: []
            }
        ];
        this.renderFeaturedProducts();
        this.renderTrendingDeals();
    }'''

# Find where to start the replacement - at "loadProducts()"
start_idx = content.find('    loadProducts() {')
if start_idx == -1:
    print("ERROR: Could not find loadProducts() function")
    exit(1)

# Find the end of the function - look for the closing brace followed by renderFeaturedProducts
end_pattern = '    }\n\n    renderFeaturedProducts()'
end_idx = content.find(end_pattern, start_idx)
if end_idx == -1:
    print("ERROR: Could not find end of loadProducts() function")
    exit(1)

# Add the length of the closing pattern
end_idx += len('    }\n')

# Replace the function
new_content = content[:start_idx] + new_load_products + '\n\n' + content[end_idx:]

# Write the file back
with open('frontend/js/main.js', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("✓ main.js updated - now fetches products from backend API")
