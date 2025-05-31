from flask import Flask, request, render_template
import mysql.connector

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('bill_form.html')

@app.route('/generate_bill', methods=['POST'])
def generate_bill():
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

    cursor.execute("INSERT INTO customers (name) VALUES (%s)", (customer_name,))
    customer_id = cursor.lastrowid

    cursor.execute("SELECT price FROM products WHERE product_id = %s", (product_id,))
    price = cursor.fetchone()[0]
    total = price * quantity

    cursor.execute("INSERT INTO bills (customer_id, total_amount) VALUES (%s, %s)", (customer_id, total))
    bill_id = cursor.lastrowid

    cursor.execute("INSERT INTO bill_details (bill_id, product_id, quantity, subtotal) VALUES (%s, %s, %s, %s)",
                   (bill_id, product_id, quantity, total))

    connection.commit()
    cursor.close()
    connection.close()

    return f"Bill generated successfully. Total amount: ₹{total}"

if __name__ == '__main__':
    app.run(debug=True)
