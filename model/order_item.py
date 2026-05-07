

class OrderItem:
    def __init__(self, id: int, order_id: int, product_id: int, quantity: int, sum_price: int):
        self.id = id
        self.order_id = order_id
        self.product_id = product_id
        self.quantity = quantity
        self.sum_price = sum_price
    

    def __repr__(self):
        return f"OrderItem(id={self.id}, order_id='{self.order_id}', product_id='{self.product_id}', quantity='{self.quantity}', sum_price='{self.sum_price}')"