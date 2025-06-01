from flask import Flask, render_template, request, redirect, url_for, session
from db import *
from flask import flash

app = Flask(__name__)
app.secret_key = "super-secret-key"  # Change this to a secure key in production

@app.route('/')
def home():
    if 'user' in session:
        return render_template('home.html', username=session['user'])
    return redirect(url_for('login'))

@app.route('/admin/products', methods=['GET', 'POST'])
def manage_products():
    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        action = request.form['action']

        if action == 'add':
            name = request.form['name']
            price = float(request.form['price'])
            add_product(name, price)

        elif action == 'update':
            product_id = request.form['id']
            name = request.form['name']
            price = float(request.form['price'])
            update_product(product_id, name, price)

        elif action == 'delete':
            product_id = request.form['id']
            delete_product(product_id)

        return redirect(url_for('manage_products'))

    products = get_all_products()
    return render_template('products.html', products=products)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = validate_user(request.form['username'], request.form['password'])
        if user:
            session['user'] = user['username']
            return redirect(url_for('home'))
        else:
            flash("Invalid username or password")
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        register_user(request.form['username'], request.form['password'])
        flash("Registered successfully! Please login.")
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/create_invoice', methods=['GET', 'POST'])
def create_invoice():
    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Get customer details from form
        customer_name = request.form['customer_name']
        customer_phone = request.form['customer_phone']

        # Save customer, get customer_id
        customer_id = add_customer(customer_name, customer_phone)

        # Create invoice for customer, get invoice_id
        invoice_id = insert_invoice(customer_id)

        # Add invoice items
        product_ids = request.form.getlist('product_id')
        quantities = request.form.getlist('quantity')

        for pid, qty in zip(product_ids, quantities):
            add_invoice_item(invoice_id, int(pid), int(qty))

        # Fetch full invoice details to display
        invoice_data =  get_invoice_details(invoice_id)

        # Render invoice display page
        return render_template('invoice_display.html', invoice=invoice_data)

    # GET request: show create invoice form
    products = get_all_products()
    return render_template('create_invoice.html', products=products)



@app.route('/invoice/<int:invoice_id>')
def view_invoice(invoice_id):
    if 'user' not in session:
        return redirect(url_for('login'))

    invoice, items = get_invoice(invoice_id)
    if not invoice:
        return "Invoice not found", 404
    return render_template('invoice.html', invoice=invoice, items=items)

if __name__ == '__main__':
    app.run(debug=True)
