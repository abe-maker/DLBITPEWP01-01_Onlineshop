import sqlite3
from .user import User
from .product import Product
from .category import Category
from .order import Order
from .order_item import OrderItem

class DatabaseManager:
    def __init__(self, db_path="shop.db"):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self):
        # Erlaubt den Zugriff auf Spalten per Name (row['name']) statt Index (row[1])
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        """Erstellt die Tabellen gemäß deinem Datenmodell."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Kategorien
            cursor.execute('''CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT)''')

            # Produkte
            cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                price REAL NOT NULL,
                category_id INTEGER,
                FOREIGN KEY (category_id) REFERENCES categories (id))''')

            # Nutzer
            cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL)''')

            # Bestellungen
            cursor.execute('''CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                total_price REAL,
                status TEXT,
                FOREIGN KEY (user_id) REFERENCES users (id))''')

            # Bestellpositionen
            cursor.execute('''CREATE TABLE IF NOT EXISTS order_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER,
                product_id INTEGER,
                quantity INTEGER,
                sum_price REAL,
                FOREIGN KEY (order_id) REFERENCES orders (id),
                FOREIGN KEY (product_id) REFERENCES products (id))''')
            
            conn.commit()

    # --- BEISPIEL-METHODEN FÜR DEN MVP ---

    def add_product(self, product: Product):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO products (name, description, price, category_id) VALUES (?, ?, ?, ?)",
                (product.name, product.description, product.price, product.category_id)
            )
            conn.commit()

    def get_all_products(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM products")
            rows = cursor.fetchall()
            # Mapping zurück in deine Product-Klasse
            return [Product(row['id'], row['name'], row['description'], 
                            row['price'], row['category_id']) for row in rows]
        
    def get_product_by_id(self, product_id):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM products WHERE product_id = ?", (product_id,))
            row = cursor.fetchone()
            if row:
                return Product(
                    id=row['id'], 
                    name=row['name'], 
                    description=row['description'], 
                    price=row['price'], 
                    category_id=row['category_id']
                )
            return None
            

    def get_products_by_category(self, category_id):        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM products WHERE category_id = ?", (category_id,))
            rows = cursor.fetchall()
            return [Product(row['id'], row['name'], row['description'], 
                            row['price'], row['category_id']) for row in rows]

    def get_user_by_email(self, email):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
            row = cursor.fetchone()
            if row:
                return User(row['id'], row['name'], row['email'], row['password'], row['role'])
            return None