from .product import Product

class OrderItem:
    def __init__(self, id: int, order_id: int, product_id: int, quantity: int, sum_price: int):
        self.id = id
        self.order_id = order_id
        self.product_id = product_id
        self.quantity = quantity
        self.sum_price = sum_price
    

    def calculate_sum_price(self, price_per_unit):
        #Berechnet den Preis der Position
        self.sum_price = self.quantity * price_per_unit
    
    def __repr__(self):
        return f"OrderItem(id={self.id}, order_id='{self.order_id}', product_id='{self.product_id}', quantity='{self.quantity}', sum_price='{self.sum_price}')"