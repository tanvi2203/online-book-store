import os

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "bookstore")

SECRET_KEY = os.getenv("SECRET_KEY", "change-this-secret-key")

ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@bookstore.com")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")
