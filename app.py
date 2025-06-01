from flask import Flask, request, render_template, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = '5f77ef8c037b9812d07f3e58968b1d73f38aad31a9492fe09e516cc50ecdfb00'

def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='181192',
        database='billing'
    )

@app.route('/')
def index():
    if 'role' in session:
        if session['role'] == 'admin':
            return redirect(url_for('admin_page'))
        elif session['role'] == 'user':
            return redirect(url_for('user_page'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    registered = request.args.get('registered')
    if registered == 'true':
        "Registration successful! Please log in."
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == '$pbkdf2-sha256$29000$DY4RffL6WZKoQvlRkT3jMw$gdroG3iRxFV1Kf7eWHDyHR2d7nExFzPMzmGkSfGAkPY':
            session['role'] = 'admin'
            return render_template('admin_d.html')
        elif username == 'user' and password == '$pbkdf2-sha256$29000$03RhqW7Z4go5AwS06pIvqQ$F5bBYy5QUddoZQRoJVprkL9X2EuTGAdFwTfaaEKOfy4':
            session['role'] = 'user'
            return redirect(url_for('user_page'))
        else:
            error = 'Invalid credentials'
    return render_template('login.html', error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        connection = get_db_connection()
        cursor = connection.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            connection.commit()
            cursor.close()
            connection.close()
            return redirect(url_for('login', registered='true'))
        except mysql.connector.IntegrityError:
            error = "Username already exists."
            cursor.close()
            connection.close()
    return render_template('register.html', error=error)

@app.route('/admin', methods=['GET'])
def admin_page():
    if session.get('role') != 'admin':
        return redirect(url_for('login'))
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT id, name, price FROM products")
    products = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('admin_d.html', products=products)

@app.route('/add_product', methods=['POST'])
def add_product():
    if session.get('role') != 'admin':
        return redirect(url_for('login'))
    name = request.form['name']
    price = float(request.form['price'])
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO products (name, price) VALUES (%s, %s)", (name, price))
    connection.commit()
    cursor.close()
    connection.close()
    return redirect(url_for('admin_page'))

@app.route('/edit_product/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    if session.get('role') != 'admin':
        return redirect(url_for('login'))
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])
        cursor.execute("UPDATE products SET name=%s, price=%s WHERE id=%s", (name, price, product_id))
        connection.commit()
        cursor.close()
        connection.close()
        return redirect(url_for('admin_page'))
    else:
        cursor.execute("SELECT id, name, price FROM products WHERE id=%s", (product_id,))
        product = cursor.fetchone()
        cursor.close()
        connection.close()
        return render_template('edit_product.html', product=product)

@app.route('/delete_product/<int:product_id>')
def delete_product(product_id):
    if session.get('role') != 'admin':
        return redirect(url_for('login'))
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM products WHERE id=%s", (product_id,))
    connection.commit()
    cursor.close()
    connection.close()
    return redirect(url_for('admin_page'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/user')
def user_page():
    if session.get('role') != 'user':
        return redirect(url_for('login'))
    return render_template('user_page.html')

@app.route('/generate_bill', methods=['POST'])
def generate_bill():
    customer_name = request.form['customerName']
    product_id = int(request.form['productId'])
    quantity = int(request.form['quantity'])

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("INSERT INTO customers (name) VALUES (%s)", (customer_name,))
    customer_id = cursor.lastrowid

    cursor.execute("SELECT name, price FROM products WHERE product_id = %s", (product_id,))
    product = cursor.fetchone()
    product_name, price = product
    total = price * quantity

    cursor.execute("INSERT INTO bills (customer_id, total_amount) VALUES (%s, %s)", (customer_id, total))
    bill_id = cursor.lastrowid

    cursor.execute("INSERT INTO bill_details (bill_id, product_id, quantity, subtotal) VALUES (%s, %s, %s, %s)",
                   (bill_id, product_id, quantity, total))

    connection.commit()
    cursor.close()
    connection.close()

    return render_template('invoice.html',
                           customer_name=customer_name,
                           product_name=product_name,
                           price=price,
                           quantity=quantity,
                           total=total,
                           bill_id=bill_id)

if __name__ == '__main__':
    app.run(debug=True)


