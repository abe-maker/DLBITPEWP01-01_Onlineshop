

class Category:
    def __init__(self, id: int, name: str, description: str):
        self.id = id
        self.name = name
        self.description = description


    def __repr__(self):
        return f"User(id={self.id}, name='{self.name}', email='{self.email}', role='{self.role}')"