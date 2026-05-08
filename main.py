from model.database import DatabaseManager
from model.product import Product
from model.category import Category
from model.user import User
from model.order import Order

def main():
    db = DatabaseManager("shop_test.db")
    print("Datenbank erfolgreich initialisiert.")

    Buch = Product(
        id=None, 
        name="Python Buch", 
        description="Lerne Programmieren", 
        price=29.99, 
        category_id=1
    )

    Auto = Product(
        id=None, 
        name="Auto", 
        description="Fiat Barchetta", 
        price=3500, 
        category_id=2
    )

    firstOrder = Order(id = None, user_id = 1, status = "offen")
    firstOrder.add_item(Auto)
    firstOrder.add_item(Buch)
    for item in firstOrder.items:
        print(item)

    
    

if __name__ == "__main__":
    main()