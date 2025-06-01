from flask import Flask, render_template, request, redirect, url_for, session
from db import *
from flask import flash

app = Flask(__name__)
app.secret_key = "super-secret-key"  # Change this to a secure key in production

@app.route('/')
def home():
    # if 'user' in session:
    #     return render_template('home.html', username=session['user'])
    return redirect(url_for('login'))

@app.route('/admin_page', methods=['GET'])
def admin_page():
    if 'user' not in session:
        return redirect(url_for('login'))

    user_role = get_user_role(session['user'])
    if user_role != 'admin':
        return "Unauthorized", 403

    return render_template('admin.html')

@app.route('/manage_products', methods=['GET', 'POST'])
def manage_products():
    if 'user' not in session:
        return redirect(url_for('login'))

    user_role = get_user_role(session['user'])
    if user_role != 'admin':
        return "Unauthorized", 403

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
    return render_template('manage_products.html', products=products)

@app.route('/manage_staff', methods=['GET', 'POST'])
def manage_staff():
    if 'user' not in session:
        return redirect(url_for('login'))

    user_role = get_user_role(session['user'])
    if user_role != 'admin':
        return "Unauthorized", 403

    if request.method == 'POST':
        action = request.form['action']

        if action == 'add_staff':
            username = request.form['username']
            password = request.form['password']
            add_staff(username, password)

        elif action == 'update_staff':
            staff_id = request.form['id']
            username = request.form['username']
            update_staff(staff_id, username)

        elif action == 'delete_staff':
            staff_id = request.form['id']
            delete_staff(staff_id)

        elif action == 'reset_password':
            staff_id = request.form['staff_id']
            new_password = request.form['new_password']
            reset_staff_password(staff_id, new_password)

        return redirect(url_for('manage_staff'))

    staffs = get_all_staffs()
    return render_template('manage_staff.html', staffs=staffs)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = validate_user(request.form['username'], request.form['password'])
        if user:
            session['user'] = user['username']
            user_role = get_user_role(user['username'])
            if user_role == 'admin':
                return redirect(url_for('manage_products'))
            elif user_role == 'staff':
                return redirect(url_for('create_invoice'))
        else:
            flash("Invalid username or password")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/create_invoice', methods=['GET', 'POST'])
def create_invoice():
    if 'user' not in session:
        return redirect(url_for('login'))

    user_role = get_user_role(session['user'])
    if user_role != 'staff':
        return "Unauthorized", 403

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
