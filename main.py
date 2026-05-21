from model.database import DatabaseManager
from model.product import Product
from model.category import Category
from model.user import User
from model.order import Order

from controller import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)


# def main():
#     db = DatabaseManager("shop_test.db")
#     print("Datenbank erfolgreich initialisiert.")

#     Auto = Product(
#             id = None,
#             name = "Porsche",
#             description = "cool",
#             price = 100,
#             category_id = 1
#     )
    

#     db.add_product(Auto)

#     firstOrder = Order(
#         id = None,
#         user_id = 1,
#         status = "offen"
#     )
#     firstOrder.add_item(Auto)

#     db.add_order(firstOrder)

# if __name__ == "__main__":
#     main()