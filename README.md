# Billing System

## Project Overview
The Billing System is a web application designed to streamline the process of managing products, customers, and invoices. It provides an intuitive interface for admins and staff to perform essential billing operations efficiently.

## Features
- **Admin Dashboard**: Manage products and staff.
- **Product Management**: Add, update, and delete products.
- **Staff Management**: Add, update, delete staff, and reset passwords.
- **Invoice Creation**: Generate invoices for customers with selected products and quantities.
- **Invoice Display**: View detailed invoices with product breakdowns and total amounts.
- **Authentication**: Secure login for admins and staff.

## Setup Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/Sananta-0902/BMS_py.git
   cd BMS_py
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up the database:
   - Import the SQL schema from `Schema.sql` into your MySQL database.
   - Update the database connection details (`username`,`password`) in `db.py`.

4. Run the `admin_setup.py` to create an admin
   ```bash
   python admin_setup.py
   ```

5. Run the application:
   ```bash
   python app.py
   ```

6. Access the application:
   - Open your browser and navigate to `http://127.0.0.1:5000`.

## Database Schema
The database schema is defined in the `billing_system.sql` file. It includes tables for:
- `users`: Admin and staff authentication.
- `products`: Product management.
- `customers`: Customer details.
- `invoices`: Invoice generation.
- `invoice_items`: Items in each invoice.

## Technologies Used
- **Backend**: Python (Flask)
- **Frontend**: HTML, CSS, Bootstrap
- **Database**: MySQL
- **Authentication**: Werkzeug for password hashing

