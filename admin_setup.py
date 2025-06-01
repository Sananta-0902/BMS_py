from werkzeug.security import generate_password_hash
from db import get_db_connection

def insert_admin_user(username='admin', password='admin'):
    db = get_db_connection()
    cursor = db.cursor()

    # Check if admin already exists
    cursor.execute("SELECT id FROM users WHERE username = %s AND role = %s", (username, 'admin'))
    if cursor.fetchone():
        print(f"⚠️ Admin user '{username}' already exists.")
        db.close()
        return

    hashed_password = generate_password_hash(password)
    cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)", 
                   (username, hashed_password, 'admin'))
    db.commit()
    db.close()
    print(f"✅ Admin user '{username}' inserted successfully.")

# Optional: run directly if script is executed
if __name__ == "__main__":
    insert_admin_user()
