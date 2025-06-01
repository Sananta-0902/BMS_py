import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="edwinpaul1811",  # ← Replace with your MySQL password
        database="billing_db"
    )

# User functions
def register_user(username, password):
    db = get_db_connection()
    cursor = db.cursor()
    hashed = generate_password_hash(password)
    cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed))
    db.commit()
    db.close()

def validate_user(username, password):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    db.close()
    if user and check_password_hash(user['password'], password):
        return user
    return None

# Invoice-related functions
def get_customers():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM customers")
    result = cursor.fetchall()
    db.close()
    return result

def get_products():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products")
    result = cursor.fetchall()
    db.close()
    return result

def insert_invoice(customer_id, product_ids, quantities):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("INSERT INTO invoices (customer_id) VALUES (%s)", (customer_id,))
    invoice_id = cursor.lastrowid

    for pid, qty in zip(product_ids, quantities):
        cursor.execute("""
            INSERT INTO invoice_items (invoice_id, product_id, quantity)
            VALUES (%s, %s, %s)
        """, (invoice_id, pid, qty))

    db.commit()
    db.close()
    return invoice_id

def get_invoice(invoice_id):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT invoices.id, invoices.date, customers.name, customers.email, customers.phone
        FROM invoices
        JOIN customers ON invoices.customer_id = customers.id
        WHERE invoices.id = %s
    """, (invoice_id,))
    invoice = cursor.fetchone()

    cursor.execute("""
        SELECT products.name, products.price, invoice_items.quantity
        FROM invoice_items
        JOIN products ON invoice_items.product_id = products.id
        WHERE invoice_items.invoice_id = %s
    """, (invoice_id,))
    items = cursor.fetchall()

    db.close()
    return invoice, items
