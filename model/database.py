import sqlite3
from .user import User
from .product import Product
from .category import Category
from .order import Order
from .order_item import OrderItem

class DatabaseManager:
    def __init__(self, db_path="shop.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path, timeout = 20)
        self.conn.row_factory = sqlite3.Row
        self._init_db()

    def close(self):
        self.conn.close()
        self.conn = None
    

    def _init_db(self):
        """Erstellt die Tabellen gemäß deinem Datenmodell."""

        cursor = self.conn.cursor()
        
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
            status TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id))''')

        # Bestellpositionen
        cursor.execute('''CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER,
            product_id INTEGER,
            quantity INTEGER,
            FOREIGN KEY (order_id) REFERENCES orders (id),
            FOREIGN KEY (product_id) REFERENCES products (id))''')
        
        self.conn.commit()

    # Methoden

    def add_product(self, product):
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO products (name, description, price, category_id) VALUES (?, ?, ?, ?)",
            (product.name, product.description, product.price, product.category_id)
        )
        self.conn.commit()
        #gibt den neuen Primärschlussel zurück
        product.id = cursor.lastrowid


    def remove_product(self, product):
        cursor = self.conn.cursor()
        cursor.execute(
            "DELETE FROM products WHERE id = ?", (product.id,)
        )
        self.conn.commit()

    def get_all_products(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM products")
        rows = cursor.fetchall()
        # Mapping zurück in deine Product-Klasse
        return [Product(row['id'], row['name'], row['description'], 
                        row['price'], row['category_id']) for row in rows]
        
    def get_product_by_id(self, product_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
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
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM products WHERE category_id = ?", (category_id,))
        rows = cursor.fetchall()
        return [Product(row['id'], row['name'], row['description'], 
                        row['price'], row['category_id']) for row in rows]

        
    def get_order_by_id(self, order_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
        row = cursor.fetchone()
        if not row:
            return None
        items = self.get_order_items_by_order(order_id)
        return Order(row['id'], row['user_id'], row['status'], items)

    def add_order(self, order: Order):
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO orders (user_id, status) VALUES (?, ?)",
            (order.user_id, order.status),
        )
        order.id = cursor.lastrowid
        for item in order.items:
            item.order_id = order.id
            self.add_order_item(item)
        self.conn.commit()
        return order.id

    def add_order_item(self, order_item: OrderItem):
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO order_items (order_id, product_id, quantity) VALUES (?, ?, ?)",
            (order_item.order_id, order_item.product_id, order_item.quantity),
        )
        order_item.id = cursor.lastrowid
        self.conn.commit()
        return order_item.id