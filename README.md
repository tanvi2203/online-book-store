# Online Book Store

This is a simple Online Book Store project made as a full-stack web application.

The project allows users to view books, search for books, add books to a cart, place orders, and check their previous orders.

There is also an admin section where the admin can manage books and orders.

## Technologies Used

### Frontend

* HTML
* CSS
* JavaScript
* React.js

### Backend

* Python
* Flask

### Database

* MySQL

## Main Features

### User

* Register
* Login and Logout
* View books
* Search books
* View book details
* Add books to cart
* Update cart quantity
* Remove books from cart
* Place orders
* View orders
* View order details

### Admin

* Admin login
* View dashboard
* Add books
* Delete books
* View all orders
* Update order status
* View users

## Project Structure

```text
online-book-store
│
├── backend
│   ├── app.py
│   ├── database.py
│   ├── config.py
│   └── requirements.txt
│
├── frontend
│   ├── src
│   ├── public
│   ├── package.json
│   └── vite.config.js
│
├── database
│   └── bookstore.sql
│
└── README.md
```

## How to Run the Project

### 1. Start MySQL

Make sure MySQL is installed and running on your computer.

### 2. Run the Backend

Open the terminal in VS Code:

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

Install the required packages:

```bash
pip install -r requirements.txt
```

Run the Flask server:

```bash
python app.py
```

The backend will run on:

```text
http://localhost:5000
```

### 3. Run the Frontend

Open another terminal:

```bash
cd frontend
```

Install the packages:

```bash
npm install
```

Start the React application:

```bash
npm run dev
```

The frontend will run on:

```text
http://localhost:5173
```

## Admin Login

For testing the admin section:

```text
Email: admin@bookstore.com
Password: admin123
```

The password can be changed later.

## Database

The project uses MySQL.

The database and required tables are created when the backend starts.

The SQL file is also available in:

```text
database/bookstore.sql
```

## Note

This is a student project created for learning full-stack web development.

It is a basic online book store and does not include a real payment gateway.

## Learning

This project helped me understand:

* React.js
* Flask
* MySQL
* REST APIs
* Frontend and backend communication
* Database operations
* User login and sessions
* Shopping cart
* Order management
