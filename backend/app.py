from decimal import Decimal
from functools import wraps

from flask import Flask, jsonify, request, session
from werkzeug.security import generate_password_hash, check_password_hash

from config import SECRET_KEY, ADMIN_EMAIL, ADMIN_PASSWORD
from database import get_connection, init_database, seed_books

app = Flask(__name__)
app.secret_key = SECRET_KEY
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"


def money(value):
    return float(value) if isinstance(value, Decimal) else value


def user_from_session():
    user_id = session.get("user_id")
    if not user_id:
        return None

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(
        "SELECT id, name, email, role FROM users WHERE id = %s",
        (user_id,),
    )
    user = cursor.fetchone()
    cursor.close()
    connection.close()
    return user


def login_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if not session.get("user_id"):
            return jsonify({"message": "Please login first"}), 401
        return function(*args, **kwargs)

    return wrapper


def admin_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        user = user_from_session()
        if not user:
            return jsonify({"message": "Please login first"}), 401
        if user["role"] != "admin":
            return jsonify({"message": "Admin access required"}), 403
        return function(*args, **kwargs)

    return wrapper


@app.route("/api/health")
def health():
    return jsonify({"message": "Book Store API is running"})


# ---------------- AUTHENTICATION ----------------

@app.route("/api/register", methods=["POST"])
def register():
    data = request.get_json() or {}

    name = data.get("name", "").strip()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not name or not email or not password:
        return jsonify({"message": "All fields are required"}), 400

    if len(password) < 4:
        return jsonify({"message": "Password must contain at least 4 characters"}), 400

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
    if cursor.fetchone():
        cursor.close()
        connection.close()
        return jsonify({"message": "Email already registered"}), 409

    hashed_password = generate_password_hash(password)

    cursor.execute(
        "INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, 'user')",
        (name, email, hashed_password),
    )
    connection.commit()

    user_id = cursor.lastrowid
    cursor.close()
    connection.close()

    session["user_id"] = user_id

    return jsonify({
        "message": "Registration successful",
        "user": {
            "id": user_id,
            "name": name,
            "email": email,
            "role": "user",
        },
    }), 201


@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json() or {}

    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    cursor.close()
    connection.close()

    if not user or not check_password_hash(user["password"], password):
        return jsonify({"message": "Invalid email or password"}), 401

    session["user_id"] = user["id"]

    return jsonify({
        "message": "Login successful",
        "user": {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
            "role": user["role"],
        },
    })


@app.route("/api/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"message": "Logged out successfully"})


@app.route("/api/user")
def current_user():
    user = user_from_session()
    return jsonify({"user": user})


# ---------------- BOOKS ----------------

@app.route("/api/books", methods=["GET"])
def get_books():
    search = request.args.get("search", "").strip()
    category = request.args.get("category", "").strip()

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT id, title, author, category, price, description, image, stock
        FROM books
        WHERE 1 = 1
    """
    values = []

    if search:
        query += " AND (title LIKE %s OR author LIKE %s)"
        values.extend([f"%{search}%", f"%{search}%"])

    if category:
        query += " AND category = %s"
        values.append(category)

    query += " ORDER BY id DESC"

    cursor.execute(query, values)
    books = cursor.fetchall()

    cursor.close()
    connection.close()

    for book in books:
        book["price"] = money(book["price"])

    return jsonify(books)


@app.route("/api/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM books WHERE id = %s", (book_id,))
    book = cursor.fetchone()
    cursor.close()
    connection.close()

    if not book:
        return jsonify({"message": "Book not found"}), 404

    book["price"] = money(book["price"])
    return jsonify(book)


# ---------------- CART ----------------

@app.route("/api/cart", methods=["GET"])
@login_required
def get_cart():
    user_id = session["user_id"]

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            cart.id,
            cart.book_id,
            cart.quantity,
            books.title,
            books.author,
            books.price,
            books.image,
            books.stock,
            (cart.quantity * books.price) AS subtotal
        FROM cart
        JOIN books ON books.id = cart.book_id
        WHERE cart.user_id = %s
        ORDER BY cart.id DESC
    """, (user_id,))

    items = cursor.fetchall()
    cursor.close()
    connection.close()

    total = 0
    for item in items:
        item["price"] = money(item["price"])
        item["subtotal"] = money(item["subtotal"])
        total += item["subtotal"]

    return jsonify({"items": items, "total": total})


@app.route("/api/cart", methods=["POST"])
@login_required
def add_to_cart():
    data = request.get_json() or {}
    book_id = data.get("book_id")
    quantity = int(data.get("quantity", 1))

    if not book_id or quantity < 1:
        return jsonify({"message": "Invalid cart data"}), 400

    user_id = session["user_id"]

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT id, stock FROM books WHERE id = %s", (book_id,))
    book = cursor.fetchone()

    if not book:
        cursor.close()
        connection.close()
        return jsonify({"message": "Book not found"}), 404

    cursor.execute(
        "SELECT quantity FROM cart WHERE user_id = %s AND book_id = %s",
        (user_id, book_id),
    )
    existing = cursor.fetchone()

    new_quantity = quantity + (existing["quantity"] if existing else 0)

    if new_quantity > book["stock"]:
        cursor.close()
        connection.close()
        return jsonify({"message": "Not enough stock"}), 400

    if existing:
        cursor.execute(
            "UPDATE cart SET quantity = %s WHERE user_id = %s AND book_id = %s",
            (new_quantity, user_id, book_id),
        )
    else:
        cursor.execute(
            "INSERT INTO cart (user_id, book_id, quantity) VALUES (%s, %s, %s)",
            (user_id, book_id, quantity),
        )

    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({"message": "Book added to cart"}), 201


@app.route("/api/cart/<int:cart_id>", methods=["PUT"])
@login_required
def update_cart(cart_id):
    data = request.get_json() or {}
    quantity = int(data.get("quantity", 1))

    if quantity < 1:
        return jsonify({"message": "Quantity must be at least 1"}), 400

    user_id = session["user_id"]

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT cart.id, books.stock
        FROM cart
        JOIN books ON books.id = cart.book_id
        WHERE cart.id = %s AND cart.user_id = %s
    """, (cart_id, user_id))

    item = cursor.fetchone()

    if not item:
        cursor.close()
        connection.close()
        return jsonify({"message": "Cart item not found"}), 404

    if quantity > item["stock"]:
        cursor.close()
        connection.close()
        return jsonify({"message": "Not enough stock"}), 400

    cursor.execute(
        "UPDATE cart SET quantity = %s WHERE id = %s AND user_id = %s",
        (quantity, cart_id, user_id),
    )
    connection.commit()

    cursor.close()
    connection.close()

    return jsonify({"message": "Cart updated"})


@app.route("/api/cart/<int:cart_id>", methods=["DELETE"])
@login_required
def delete_cart(cart_id):
    user_id = session["user_id"]

    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "DELETE FROM cart WHERE id = %s AND user_id = %s",
        (cart_id, user_id),
    )
    connection.commit()

    deleted = cursor.rowcount
    cursor.close()
    connection.close()

    if deleted == 0:
        return jsonify({"message": "Cart item not found"}), 404

    return jsonify({"message": "Item removed from cart"})


# ---------------- ORDERS ----------------

@app.route("/api/orders", methods=["POST"])
@login_required
def create_order():
    user_id = session["user_id"]

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        connection.start_transaction()

        cursor.execute("""
            SELECT
                cart.book_id,
                cart.quantity,
                books.price,
                books.stock,
                books.title
            FROM cart
            JOIN books ON books.id = cart.book_id
            WHERE cart.user_id = %s
            FOR UPDATE
        """, (user_id,))

        cart_items = cursor.fetchall()

        if not cart_items:
            connection.rollback()
            return jsonify({"message": "Your cart is empty"}), 400

        total = Decimal("0.00")

        for item in cart_items:
            if item["quantity"] > item["stock"]:
                connection.rollback()
                return jsonify({
                    "message": f"Not enough stock for {item['title']}"
                }), 400
            total += item["price"] * item["quantity"]

        cursor.execute(
            "INSERT INTO orders (user_id, total_amount) VALUES (%s, %s)",
            (user_id, total),
        )
        order_id = cursor.lastrowid

        for item in cart_items:
            cursor.execute("""
                INSERT INTO order_items
                (order_id, book_id, quantity, price)
                VALUES (%s, %s, %s, %s)
            """, (
                order_id,
                item["book_id"],
                item["quantity"],
                item["price"],
            ))

            cursor.execute("""
                UPDATE books
                SET stock = stock - %s
                WHERE id = %s
            """, (item["quantity"], item["book_id"]))

        cursor.execute("DELETE FROM cart WHERE user_id = %s", (user_id,))
        connection.commit()

        return jsonify({
            "message": "Order placed successfully",
            "order_id": order_id,
            "total": float(total),
        }), 201

    except Exception as error:
        connection.rollback()
        return jsonify({"message": "Could not place order", "error": str(error)}), 500

    finally:
        cursor.close()
        connection.close()


@app.route("/api/orders", methods=["GET"])
@login_required
def get_orders():
    user_id = session["user_id"]

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("""
        SELECT id, total_amount, status, order_date
        FROM orders
        WHERE user_id = %s
        ORDER BY order_date DESC
    """, (user_id,))
    orders = cursor.fetchall()
    cursor.close()
    connection.close()

    for order in orders:
        order["total_amount"] = money(order["total_amount"])

    return jsonify(orders)


@app.route("/api/orders/<int:order_id>", methods=["GET"])
@login_required
def get_order(order_id):
    user_id = session["user_id"]

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT id, total_amount, status, order_date
        FROM orders
        WHERE id = %s AND user_id = %s
    """, (order_id, user_id))

    order = cursor.fetchone()

    if not order:
        cursor.close()
        connection.close()
        return jsonify({"message": "Order not found"}), 404

    cursor.execute("""
        SELECT
            order_items.quantity,
            order_items.price,
            books.title,
            books.author,
            books.image
        FROM order_items
        JOIN books ON books.id = order_items.book_id
        WHERE order_items.order_id = %s
    """, (order_id,))

    items = cursor.fetchall()

    cursor.close()
    connection.close()

    order["total_amount"] = money(order["total_amount"])

    for item in items:
        item["price"] = money(item["price"])

    order["items"] = items
    return jsonify(order)


# ---------------- ADMIN ----------------

@app.route("/api/admin/books", methods=["POST"])
@admin_required
def admin_add_book():
    data = request.get_json() or {}

    required = ["title", "author", "category", "price", "stock"]
    if any(data.get(field) in [None, ""] for field in required):
        return jsonify({"message": "Please fill all required fields"}), 400

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO books
        (title, author, category, price, description, image, stock)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        data["title"],
        data["author"],
        data["category"],
        data["price"],
        data.get("description", ""),
        data.get("image", ""),
        int(data["stock"]),
    ))

    connection.commit()
    book_id = cursor.lastrowid
    cursor.close()
    connection.close()

    return jsonify({"message": "Book added", "book_id": book_id}), 201


@app.route("/api/admin/books/<int:book_id>", methods=["PUT"])
@admin_required
def admin_update_book(book_id):
    data = request.get_json() or {}

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE books
        SET title = %s,
            author = %s,
            category = %s,
            price = %s,
            description = %s,
            image = %s,
            stock = %s
        WHERE id = %s
    """, (
        data.get("title", ""),
        data.get("author", ""),
        data.get("category", ""),
        data.get("price", 0),
        data.get("description", ""),
        data.get("image", ""),
        int(data.get("stock", 0)),
        book_id,
    ))

    connection.commit()
    updated = cursor.rowcount

    cursor.close()
    connection.close()

    if updated == 0:
        return jsonify({"message": "Book not found"}), 404

    return jsonify({"message": "Book updated"})


@app.route("/api/admin/books/<int:book_id>", methods=["DELETE"])
@admin_required
def admin_delete_book(book_id):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("DELETE FROM books WHERE id = %s", (book_id,))
        connection.commit()

        if cursor.rowcount == 0:
            return jsonify({"message": "Book not found"}), 404

        return jsonify({"message": "Book deleted"})

    except Exception:
        connection.rollback()
        return jsonify({
            "message": "This book cannot be deleted because it is used in an existing order"
        }), 400

    finally:
        cursor.close()
        connection.close()


@app.route("/api/admin/orders", methods=["GET"])
@admin_required
def admin_get_orders():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            orders.id,
            orders.total_amount,
            orders.status,
            orders.order_date,
            users.name,
            users.email
        FROM orders
        JOIN users ON users.id = orders.user_id
        ORDER BY orders.order_date DESC
    """)

    orders = cursor.fetchall()
    cursor.close()
    connection.close()

    for order in orders:
        order["total_amount"] = money(order["total_amount"])

    return jsonify(orders)


@app.route("/api/admin/orders/<int:order_id>", methods=["PUT"])
@admin_required
def admin_update_order(order_id):
    data = request.get_json() or {}
    status = data.get("status")

    allowed_statuses = [
        "Pending",
        "Confirmed",
        "Shipped",
        "Delivered",
        "Cancelled",
    ]

    if status not in allowed_statuses:
        return jsonify({"message": "Invalid order status"}), 400

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "UPDATE orders SET status = %s WHERE id = %s",
        (status, order_id),
    )
    connection.commit()

    updated = cursor.rowcount
    cursor.close()
    connection.close()

    if updated == 0:
        return jsonify({"message": "Order not found"}), 404

    return jsonify({"message": "Order status updated"})


@app.route("/api/admin/users", methods=["GET"])
@admin_required
def admin_get_users():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT id, name, email, role, created_at
        FROM users
        ORDER BY created_at DESC
    """)

    users = cursor.fetchall()
    cursor.close()
    connection.close()

    return jsonify(users)


def create_default_admin():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT id FROM users WHERE email = %s", (ADMIN_EMAIL,))
    existing = cursor.fetchone()

    if not existing:
        cursor.execute("""
            INSERT INTO users (name, email, password, role)
            VALUES (%s, %s, %s, 'admin')
        """, (
            "Administrator",
            ADMIN_EMAIL,
            generate_password_hash(ADMIN_PASSWORD),
        ))
        connection.commit()

    cursor.close()
    connection.close()


if __name__ == "__main__":
    init_database()
    seed_books()
    create_default_admin()

    print("Backend running at http://localhost:5000")
    print(f"Default admin email: {ADMIN_EMAIL}")
    print(f"Default admin password: {ADMIN_PASSWORD}")

    app.run(debug=True, port=5000)
