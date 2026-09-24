import mysql.connector
from mysql.connector import Error
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME


def get_connection(use_database=True):
    config = {
        "host": DB_HOST,
        "user": DB_USER,
        "password": DB_PASSWORD,
    }

    if use_database:
        config["database"] = DB_NAME

    return mysql.connector.connect(**config)


def init_database():
    connection = get_connection(use_database=False)
    cursor = connection.cursor()

    cursor.execute(
        f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}` "
        "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
    )

    cursor.close()
    connection.close()

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(150) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL,
            role ENUM('user', 'admin') NOT NULL DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(200) NOT NULL,
            author VARCHAR(150) NOT NULL,
            category VARCHAR(100) NOT NULL,
            price DECIMAL(10,2) NOT NULL,
            description TEXT,
            image VARCHAR(500),
            stock INT NOT NULL DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cart (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            book_id INT NOT NULL,
            quantity INT NOT NULL DEFAULT 1,
            UNIQUE KEY unique_cart_item (user_id, book_id),
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            total_amount DECIMAL(10,2) NOT NULL,
            status ENUM('Pending', 'Confirmed', 'Shipped', 'Delivered', 'Cancelled')
                NOT NULL DEFAULT 'Pending',
            order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS order_items (
            id INT AUTO_INCREMENT PRIMARY KEY,
            order_id INT NOT NULL,
            book_id INT NOT NULL,
            quantity INT NOT NULL,
            price DECIMAL(10,2) NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
            FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE RESTRICT
        )
    """)

    connection.commit()
    cursor.close()
    connection.close()


def seed_books():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM books")
    count = cursor.fetchone()[0]

    if count == 0:
        books = [
            (
                "The Alchemist",
                "Paulo Coelho",
                "Fiction",
                399,
                "A young shepherd follows his dream and learns about purpose, courage and hope.",
                "https://images.unsplash.com/photo-1543002588-bfa74002ed7e?auto=format&fit=crop&w=500&q=80",
                20,
            ),
            (
                "Atomic Habits",
                "James Clear",
                "Self Help",
                499,
                "A practical guide to building good habits and breaking bad ones.",
                "https://images.unsplash.com/photo-1544947950-fa07a98d237f?auto=format&fit=crop&w=500&q=80",
                15,
            ),
            (
                "Clean Code",
                "Robert C. Martin",
                "Programming",
                699,
                "A guide to writing readable, maintainable and understandable software.",
                "https://images.unsplash.com/photo-1532012197267-da84d127e765?auto=format&fit=crop&w=500&q=80",
                10,
            ),
            (
                "The Psychology of Money",
                "Morgan Housel",
                "Finance",
                449,
                "Lessons about money, behavior, wealth and decision making.",
                "https://images.unsplash.com/photo-1512820790803-83ca734da794?auto=format&fit=crop&w=500&q=80",
                12,
            ),
            (
                "Harry Potter and the Philosopher's Stone",
                "J. K. Rowling",
                "Fantasy",
                599,
                "The beginning of Harry Potter's magical journey at Hogwarts.",
                "https://images.unsplash.com/photo-1511108690759-009c3d7a5f9b?auto=format&fit=crop&w=500&q=80",
                8,
            ),
        ]

        cursor.executemany("""
            INSERT INTO books
            (title, author, category, price, description, image, stock)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, books)
        connection.commit()

    cursor.close()
    connection.close()
