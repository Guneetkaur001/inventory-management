from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
import os

app.secret_key = os.urandom(24)  

products = [
    {"name": "Ladies Coat", "price": 550},
    {"name": "Gents Coat", "price": 500},
    {"name": "Hoodie", "price": 600},
    {"name": "Crop Jacket", "price": 1000},
    {"name": "Top", "price": 400},
    {"name": "Jacket", "price": 800}
]
@app.route('/')
def index():
    
    return render_template('shop.html')

@app.route("/shop", methods=['GET', 'POST'])
def shop():
   
    cart_items = session.get('cart_items', [])

    subtotal = sum(item["subtotal"] for item in cart_items)  
    tax_amount = subtotal * 0.05  
    net_bill = subtotal + tax_amount 
    if request.method == 'POST':
        pname = request.form.get('productName')
        qty = int(request.form.get('quantity'))

       
        print(f"Received product name: {pname}")
        print(f"Received quantity: {qty}")

       
        product = next((p for p in products if p["name"] == pname), None)

        if product:
            cart_item = {
                "name": product["name"],
                "price": product["price"],
                "quantity": qty,
                "subtotal": product["price"] * qty
            }

            cart_items.append(cart_item) 

            
            session['cart_items'] = cart_items
        else:
            print(f"Invalid product name: {pname}")  

    return render_template('shop.html', products=products, cart_items=cart_items, subtotal=subtotal, tax_amount=tax_amount, net_bill=net_bill)

@app.route("/clear_cart", methods=['POST'])
def clear_cart():
   
    session.pop('cart_items', None)
    return redirect(url_for('shop'))


if __name__ == "__main__":
    app.run(port=5000, debug=True)
