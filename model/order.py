

class Order:
    def __init__(self, id: int, user_id: int, total_price: int, status: str):
        self.id = id
        self.user_id = user_id
        self.total_price = total_price
        self.status = status

    
    def __repr__(self):
        return f"Order(id={self.id}, user_id='{self.user_id}', total_price='{self.total_price}', status='{self.status}')"