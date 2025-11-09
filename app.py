from flask import Flask, render_template, request, redirect, url_for, session
import json
import os

app = Flask(__name__)
app.secret_key = 'supermarket_secret_key_123'

# Sample products data
PRODUCTS = [
    {"id": 1, "name": "Milk", "price": 3.50, "category": "Dairy"},
    {"id": 2, "name": "Bread", "price": 2.00, "category": "Bakery"},
    {"id": 3, "name": "Eggs", "price": 4.00, "category": "Dairy"},
    {"id": 4, "name": "Apple", "price": 1.50, "category": "Fruits"},
    {"id": 5, "name": "Banana", "price": 1.00, "category": "Fruits"},
    {"id": 6, "name": "Rice", "price": 5.00, "category": "Grains"},
    {"id": 7, "name": "Chicken", "price": 8.00, "category": "Meat"},
    {"id": 8, "name": "Tomato", "price": 2.50, "category": "Vegetables"},
    {"id": 9, "name": "Cheese", "price": 4.50, "category": "Dairy"},
    {"id": 10, "name": "Butter", "price": 3.00, "category": "Dairy"},
    {"id": 11, "name": "Yogurt", "price": 2.50, "category": "Dairy"},
    {"id": 12, "name": "Croissant", "price": 2.50, "category": "Bakery"},
    {"id": 13, "name": "Bagel", "price": 1.50, "category": "Bakery"},
    {"id": 14, "name": "Muffin", "price": 2.00, "category": "Bakery"},
    {"id": 15, "name": "Orange", "price": 1.75, "category": "Fruits"},
    {"id": 16, "name": "Strawberry", "price": 3.00, "category": "Fruits"},
    {"id": 17, "name": "Grapes", "price": 4.00, "category": "Fruits"},
    {"id": 18, "name": "Watermelon", "price": 5.00, "category": "Fruits"},
    {"id": 19, "name": "Mango", "price": 2.50, "category": "Fruits"},
    {"id": 20, "name": "Pineapple", "price": 3.50, "category": "Fruits"},
    {"id": 21, "name": "Wheat Bread", "price": 2.50, "category": "Grains"},
    {"id": 22, "name": "Pasta", "price": 3.00, "category": "Grains"},
    {"id": 23, "name": "Oats", "price": 4.50, "category": "Grains"},
    {"id": 24, "name": "Quinoa", "price": 6.00, "category": "Grains"},
    {"id": 25, "name": "Beef", "price": 12.00, "category": "Meat"},
    {"id": 26, "name": "Pork", "price": 10.00, "category": "Meat"},
    {"id": 27, "name": "Fish", "price": 9.00, "category": "Meat"},
    {"id": 28, "name": "Salmon", "price": 15.00, "category": "Meat"},
    {"id": 29, "name": "Lettuce", "price": 2.00, "category": "Vegetables"},
    {"id": 30, "name": "Carrot", "price": 1.50, "category": "Vegetables"},
    {"id": 31, "name": "Broccoli", "price": 2.50, "category": "Vegetables"},
    {"id": 32, "name": "Potato", "price": 1.00, "category": "Vegetables"},
    {"id": 33, "name": "Onion", "price": 1.25, "category": "Vegetables"},
    {"id": 34, "name": "Cucumber", "price": 1.75, "category": "Vegetables"},
    {"id": 35, "name": "Pepper", "price": 2.00, "category": "Vegetables"},
    {"id": 36, "name": "Spinach", "price": 2.25, "category": "Vegetables"},
]

def get_categories():
    return list(set(p['category'] for p in PRODUCTS))

@app.route('/')
def index():
    category = request.args.get('category', 'All')
    if 'cart' not in session:
        session['cart'] = {}
    cart = session['cart']
    cart_items = []
    total = 0
    for product_id, quantity in cart.items():
        product = next((p for p in PRODUCTS if p['id'] == int(product_id)), None)
        if product:
            item_total = product['price'] * quantity
            total += item_total
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'total': item_total
            })
    
    filtered_products = PRODUCTS if category == 'All' else [p for p in PRODUCTS if p['category'] == category]
    categories = get_categories()
    return render_template('index.html', products=filtered_products, cart_items=cart_items, total=total, categories=categories, selected_category=category)

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    if 'cart' not in session:
        session['cart'] = {}
    cart = session['cart']
    product_id_str = str(product_id)
    cart[product_id_str] = cart.get(product_id_str, 0) + 1
    session['cart'] = cart
    category = request.args.get('category', 'All')
    return redirect(url_for('index', category=category))

@app.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    if 'cart' in session:
        cart = session['cart']
        product_id_str = str(product_id)
        if product_id_str in cart:
            cart[product_id_str] = cart[product_id_str] - 1
            if cart[product_id_str] <= 0:
                del cart[product_id_str]
            session['cart'] = cart
    category = request.args.get('category', 'All')
    return redirect(url_for('index', category=category))

@app.route('/clear_cart')
def clear_cart():
    session['cart'] = {}
    return redirect(url_for('index'))

@app.route('/checkout')
def checkout():
    if 'cart' not in session or not session['cart']:
        return redirect(url_for('index'))
    cart = session['cart']
    cart_items = []
    total = 0
    for product_id, quantity in cart.items():
        product = next((p for p in PRODUCTS if p['id'] == int(product_id)), None)
        if product:
            item_total = product['price'] * quantity
            total += item_total
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'total': item_total
            })
    session['cart'] = {}
    categories = get_categories()
    return render_template('checkout.html', cart_items=cart_items, total=total, categories=categories)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

