from model.database import DatabaseManager
from model.product import Product
from model.category import Category
from model.user import User
from model.order import Order

from controller import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)