from flask import Blueprint, render_template, request

# Use absolute imports so running the app as a script resolves correctly
from model.database import DatabaseManager

# Avoid circular import: define DB file name here (matches controller.__init__.py)
DB_NAME = "database.db"


views = Blueprint("views", __name__)


@views.route("/")
def home():
    return render_template("home.html")


@views.route('/product-list')
def product_list():
    # optional category filter via ?category=<id>
    category_id = request.args.get('category')
    db = DatabaseManager(DB_NAME)
    try:
        if category_id:
            try:
                cid = int(category_id)
            except ValueError:
                cid = None
            products = db.get_products_by_category(cid) if cid else db.get_all_products()
        else:
            products = db.get_all_products()

        categories = db.get_all_categories()
    finally:
        db.close()

    return render_template('product-list.html', products=products, categories=categories)


@views.route('/cart')
def cart():
    return render_template('cart.html')


@views.route('/login')
def login():
    return render_template('login.html')