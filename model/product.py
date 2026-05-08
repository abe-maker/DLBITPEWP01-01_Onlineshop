

class Product:
    def __init__(self, id: int, name: str, description: str, price: float, category_id: int):
        self.id = id
        self.name = name
        self.description = description
        self.price = price
        self.category_id = category_id


    def update_price(self, new_price: float):
        """Ändert den Produktpreis"""
        self.price = new_price


    def __repr__(self):
        return f"Product(id={self.id}, name='{self.name}', description={self.description}, price={self.price}, category_id={self.category_id})"