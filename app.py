from flask import Flask, request, render_template, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

print("Starting the billing system application...")

@app.route('/')
def index():
    return render_template('bill_form.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    connection = None
    cursor = None
    try:
        username = request.form['username']
        password = request.form['password']

        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='password',
            database='billing_system'
        )
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        if user:
            return jsonify({"message": "Login successful"}), 200
        else:
            return jsonify({"error": "Invalid credentials"}), 401

    except Error as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    connection = None
    cursor = None
    try:
        username = request.form['username']
        password = request.form['password']

        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='password',
            database='billing_system'
        )
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        if cursor.fetchone():
            return jsonify({"error": "Username already exists"}), 400

        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        connection.commit()
        return jsonify({"message": "Registration successful"}), 201

    except Error as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

@app.route('/generate_bill', methods=['POST'])
def generate_bill():
    connection = None
    cursor = None
    try:
        customer_name = request.form['customerName']
        product_id = int(request.form['productId'])
        quantity = int(request.form['quantity'])

        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='password',
            database='billing_system'
        )
        cursor = connection.cursor()

        # Check if customer exists
        cursor.execute("SELECT customer_id FROM customers WHERE name = %s", (customer_name,))
        customer = cursor.fetchone()
        if customer:
            customer_id = customer[0]
        else:
            cursor.execute("INSERT INTO customers (name) VALUES (%s)", (customer_name,))
            customer_id = cursor.lastrowid

        cursor.execute("SELECT price FROM products WHERE product_id = %s", (product_id,))
        price_result = cursor.fetchone()
        if price_result is None:
            return jsonify({"error": "Invalid product ID"}), 400
        price = price_result[0]
        total = price * quantity

        cursor.execute("INSERT INTO bills (customer_id, total_amount) VALUES (%s, %s)", (customer_id, total))
        bill_id = cursor.lastrowid

        cursor.execute("INSERT INTO bill_details (bill_id, product_id, quantity, subtotal) VALUES (%s, %s, %s, %s)",
                       (bill_id, product_id, quantity, total))

        connection.commit()
        return jsonify({"message": "Bill generated successfully", "total_amount": float(total)}), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

if __name__ == '__main__':
    app.run(debug=True)
