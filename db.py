import pymysql
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

# DB connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="edwinpaul1811",
        database="billing_db"
    )

# ===================== USER FUNCTIONS =====================

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

# ===================== CUSTOMER FUNCTIONS =====================

def get_customers():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM customers")
    result = cursor.fetchall()
    db.close()
    return result

def insert_or_get_customer(name, phone):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT id FROM customers WHERE name=%s AND phone=%s", (name, phone))
    result = cursor.fetchone()
    if result:
        db.close()
        return result[0]

    cursor.execute("INSERT INTO customers (name, phone) VALUES (%s, %s)", (name, phone))
    db.commit()
    customer_id = cursor.lastrowid
    db.close()
    return customer_id

def add_customer(name, phone):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT id FROM customers WHERE name=%s AND phone=%s", (name, phone))
    result = cursor.fetchone()
    if result:
        db.close()
        return result[0]

    cursor.execute("INSERT INTO customers (name, phone) VALUES (%s, %s)", (name, phone))
    db.commit()
    customer_id = cursor.lastrowid
    db.close()
    return customer_id

# ===================== PRODUCT FUNCTIONS =====================

def get_all_products():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    db.close()
    return products

def get_products():
    return get_all_products()

def add_product(name, price):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("INSERT INTO products (name, price) VALUES (%s, %s)", (name, price))
    db.commit()
    db.close()

def update_product(product_id, name, price):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("UPDATE products SET name=%s, price=%s WHERE id=%s", (name, price, product_id))
    db.commit()
    db.close()

def delete_product(product_id):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("DELETE FROM products WHERE id=%s", (product_id,))
    db.commit()
    db.close()

# ===================== INVOICE FUNCTIONS =====================

def insert_invoice(customer_id, product_ids=None, quantities=None):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("INSERT INTO invoices (customer_id) VALUES (%s)", (customer_id,))
    invoice_id = cursor.lastrowid

    if product_ids and quantities:
        for pid, qty in zip(product_ids, quantities):
            cursor.execute("""
                INSERT INTO invoice_items (invoice_id, product_id, quantity)
                VALUES (%s, %s, %s)
            """, (invoice_id, pid, qty))

    db.commit()
    db.close()
    return invoice_id

def add_invoice_item(invoice_id, product_id, quantity):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("INSERT INTO invoice_items (invoice_id, product_id, quantity) VALUES (%s, %s, %s)",
                   (invoice_id, product_id, quantity))
    db.commit()
    db.close()

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

def get_invoice_details(invoice_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch invoice basic info + customer
    cursor.execute("""
        SELECT invoices.id AS invoice_id, invoices.date,
               customers.name AS customer_name, customers.phone AS customer_phone
        FROM invoices
        JOIN customers ON invoices.customer_id = customers.id
        WHERE invoices.id = %s
    """, (invoice_id,))
    invoice = cursor.fetchone()

    if not invoice:
        conn.close()
        return None  # or {} if you prefer

    # Fetch invoice items with product details
    cursor.execute("""
        SELECT products.name, products.price, invoice_items.quantity,
               (products.price * invoice_items.quantity) AS total_price
        FROM invoice_items
        JOIN products ON invoice_items.product_id = products.id
        WHERE invoice_items.invoice_id = %s
    """, (invoice_id,))
    items = cursor.fetchall()

    conn.close()

    invoice['items'] = items
    invoice['total_amount'] = sum(item['total_price'] for item in items)
    return invoice

