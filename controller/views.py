from flask import Blueprint, render_template, request, redirect, url_for, flash, session

# absolute imports
from model.database import DatabaseManager
from model.product import Product
from model.order_item import OrderItem

# defines DB
DB_NAME = "database.db"


views = Blueprint("views", __name__)


@views.route("/")
def home():
    db = DatabaseManager(DB_NAME)
    try:
        products = db.get_all_products()
    finally:
        db.close()

    return render_template("home.html", products=products)


@views.route('/product-list')
def product_list():
    # category filter
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


@views.route('/admin', methods=['GET', 'POST'])
def admin():
    db = DatabaseManager(DB_NAME)
    try:
        if request.method == 'POST':
            if request.form.get('add_product'):
                name = request.form.get('name', '').strip()
                description = request.form.get('description', '').strip()
                price = request.form.get('price', '').strip()
                category_id = request.form.get('category_id')

                if not name or not price:
                    flash('Name und Preis sind erforderlich.', 'error')
                    return redirect(url_for('views.admin'))

                try:
                    price_value = float(price)
                except ValueError:
                    flash('Preis muss eine Zahl sein.', 'error')
                    return redirect(url_for('views.admin'))

                if category_id:
                    try:
                        category_id = int(category_id)
                    except ValueError:
                        category_id = None
                else:
                    category_id = None

                product = Product(id=None, name=name, description=description, price=price_value, category_id=category_id)
                db.add_product(product)
                flash(f'Produkt "{name}" hinzugefügt.', 'success')
                return redirect(url_for('views.admin'))

            if request.form.get('delete_product'):
                product_id = request.form.get('product_id')
                if not product_id:
                    flash('Produkt-ID fehlt.', 'error')
                    return redirect(url_for('views.admin'))

                try:
                    db.remove_product_by_id(int(product_id))
                    flash('Produkt gelöscht.', 'success')
                except ValueError:
                    flash('Ungültige Produkt-ID.', 'error')

                return redirect(url_for('views.admin'))

        products = db.get_all_products()
        categories = db.get_all_categories()
    finally:
        db.close()

    return render_template('admin.html', products=products, categories=categories)


@views.route('/product/<int:product_id>')
def product_detail(product_id):
    db = DatabaseManager(DB_NAME)
    try:
        product = db.get_product_by_id(product_id)
    finally:
        db.close()

    if not product:
        flash('Produkt nicht gefunden.', 'error')
        return redirect(url_for('views.product_list'))

    return render_template('product-details.html', product=product)


@views.route('/cart/add', methods=['POST'])
def add_to_cart():
    """Add a product to the cart (current order)."""
    product_id = request.form.get('product_id')
    
    if not product_id:
        flash('Produkt-ID fehlt.', 'error')
        return redirect(request.referrer or url_for('views.product_list'))
    
    try:
        product_id = int(product_id)
    except ValueError:
        flash('Ungültige Produkt-ID.', 'error')
        return redirect(request.referrer or url_for('views.product_list'))
    
    db = DatabaseManager(DB_NAME)
    try:
        product = db.get_product_by_id(product_id)
        if not product:
            flash('Produkt nicht gefunden.', 'error')
            return redirect(request.referrer or url_for('views.product_list'))
        
        # Get or create active order
        order = db.get_active_order(user_id=1)
        if not order:
            order = db.create_order(user_id=1)
        
        # Check if product is already in order
        if db.item_in_order(order.id, product_id):
            # Update quantity
            db.update_order_item_quantity(order.id, product_id, db.get_order_items_by_order(order.id)[0].quantity + 1)
            flash(f'Menge von "{product.name}" erhöht.', 'success')
        else:
            # Add new item
            order_item = OrderItem(id=None, order_id=order.id, product_id=product_id, quantity=1, unit_price=product.price)
            db.add_order_item(order_item)
            flash(f'"{product.name}" wurde in den Warenkorb gelegt.', 'success')
        
        # Store order ID in session
        session['cart_order_id'] = order.id
        
    finally:
        db.close()
    
    return redirect(url_for('views.cart'))


@views.route('/cart')
def cart():
    """Display the current cart (order items)."""
    order_id = session.get('cart_order_id')
    
    db = DatabaseManager(DB_NAME)
    try:
        order = None
        order_items = []
        
        if order_id:
            order = db.get_order_by_id(order_id)
        
        if not order:
            order = db.get_active_order(user_id=1)
            if order:
                session['cart_order_id'] = order.id
        
        if order and order.items:
            # Load product details for each item
            for item in order.items:
                product = db.get_product_by_id(item.product_id)
                if product:
                    item.unit_price = product.price
                    order_items.append({'item': item, 'product': product})
    finally:
        db.close()
    
    return render_template('cart.html', order=order, order_items=order_items)


@views.route('/cart/remove', methods=['POST'])
def remove_from_cart():
    """Remove an item from the cart."""
    item_id = request.form.get('item_id')
    
    if not item_id:
        flash('Item-ID fehlt.', 'error')
        return redirect(url_for('views.cart'))
    
    try:
        item_id = int(item_id)
    except ValueError:
        flash('Ungültige Item-ID.', 'error')
        return redirect(url_for('views.cart'))
    
    db = DatabaseManager(DB_NAME)
    try:
        db.delete_order_item(item_id)
        flash('Produkt aus dem Warenkorb entfernt.', 'success')
    finally:
        db.close()
    
    return redirect(url_for('views.cart'))


@views.route('/login')
def login():
    return render_template('login.html')



@views.route('/checkout')
def checkout():
    order_id = session.get('cart_order_id')
    db = DatabaseManager(DB_NAME)
    try:
        order = None
        order_items = []
        if order_id:
            order = db.get_order_by_id(order_id)
        if not order:
            order = db.get_active_order(user_id=1)
            if order:
                session['cart_order_id'] = order.id
        if order and order.items:
            for item in order.items:
                product = db.get_product_by_id(item.product_id)
                if product:
                    item.unit_price = product.price
                    order_items.append({'item': item, 'product': product})
    finally:
        db.close()

    return render_template('checkout.html', order=order, order_items=order_items)


@views.route('/checkout/complete', methods=['POST'])
def checkout_complete():
    name = request.form.get('name', '').strip()
    zipcode = request.form.get('zipcode', '').strip()
    city = request.form.get('city', '').strip()
    street = request.form.get('street', '').strip()
    house_number = request.form.get('house_number', '').strip()

    if not (name and zipcode and city and street and house_number):
        flash('Bitte fülle alle Felder aus.', 'error')
        return redirect(url_for('views.checkout'))

    flash('Die Bestellung wurde erfolgreich aufgenommen. Vielen Dank!', 'success')
    return redirect(url_for('views.home'))

