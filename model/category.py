

class Category:
    def __init__(self, id: int, name: str, description: str):
        self.id = id
        self.name = name
        self.description = description

    def get_products(self, db_manager):
        # Ruft Produkte direkt aus der Datenbank ab
        return db_manager.get_products_by_category(self.id)
    


    def __repr__(self):
        return f"Category(id={self.id}, name='{self.name}', description='{self.description}')"
    
