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

@app.route('/create-invoice', methods=['GET', 'POST'])
def create_invoice():
    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        customer_id = request.form['customer_id']
        product_ids = request.form.getlist('product_id')
        quantities = request.form.getlist('quantity')
        invoice_id = insert_invoice(customer_id, product_ids, quantities)
        return redirect(url_for('view_invoice', invoice_id=invoice_id))

    customers = get_customers()
    products = get_products()
    return render_template('create_invoice.html', customers=customers, products=products)

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
