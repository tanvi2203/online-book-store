# Online Book Store

A beginner-friendly full-stack online bookstore built with:

- React.js
- Flask
- MySQL
- HTML/CSS/JavaScript

No Node.js backend, Express.js, MongoDB or JWT is used.

## Features

### Customer
- Register
- Login/logout
- Browse books
- Search books
- Filter by category
- View book details
- Add to cart
- Update cart
- Remove from cart
- Checkout
- Place orders
- View order history
- View order details

### Admin
- Admin login
- Admin dashboard
- Add books
- Delete books
- View orders
- Change order status

## 1. Install requirements

You need:

- Python 3
- MySQL Server
- Node.js and npm

## 2. Backend setup

Open a terminal:

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

On macOS/Linux, activate with:

```bash
source venv/bin/activate
```

## 3. MySQL setup

Make sure MySQL Server is running.

The Flask application creates the `bookstore` database and tables automatically when it starts.

If you prefer to create the tables manually, run:

```text
database/bookstore.sql
```

## 4. Configure MySQL

The backend uses these default settings:

```text
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=
DB_NAME=bookstore
```

If your MySQL root password is not empty, set it before starting Flask.

Windows Command Prompt:

```bash
set DB_PASSWORD=your_mysql_password
```

PowerShell:

```powershell
$env:DB_PASSWORD="your_mysql_password"
```

You can also set:

```text
DB_HOST
DB_USER
DB_PASSWORD
DB_NAME
SECRET_KEY
ADMIN_EMAIL
ADMIN_PASSWORD
```

## 5. Start Flask

From the backend folder:

```bash
python app.py
```

Backend:

```text
http://localhost:5000
```

The application automatically creates sample books and a default admin.

Default admin:

```text
Email: admin@bookstore.com
Password: admin123
```

Change these values for anything beyond a local student demo.

## 6. Start React

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

Open the Vite URL shown in the terminal, normally:

```text
http://localhost:5173
```

## 7. Project flow

```text
React
  |
  | HTTP /api requests
  v
Flask
  |
  | SQL queries
  v
MySQL
```

## Notes

This is an educational project. The checkout does not process real payments.

For a production application, add stronger security controls, HTTPS, CSRF protection, stricter validation, secure production session configuration, database migrations, proper secret management, logging, testing, and a real payment provider.

## Official documentation

Flask:
https://flask.palletsprojects.com/

React:
https://react.dev/

MySQL:
https://dev.mysql.com/doc/

Vite:
https://vite.dev/
