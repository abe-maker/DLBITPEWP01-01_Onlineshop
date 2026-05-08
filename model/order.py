from .order_item import OrderItem

class Order:
    def __init__(self, id: int, user_id: int, status: str):
        self.id = id
        self.user_id = user_id
        self.status = status
        self.items = [] #Liste, die Order-Objekte speichert

    @property
    def total_price(self):
        #Berechnet die Gesamtsummer der Bestellung
        return sum(item.sum_price * item in self.items)
    
    def add_item(self, new_product):
        self.items.append(new_product)

    def remove_item(self, product):
        self.items.remove(product)

    
    def __repr__(self):
        return f"Order(id={self.id}, user_id={self.user_id}, total_price={self.total_price}, status='{self.status}')"