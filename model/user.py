

class User:
    def __init__(self, id: int, name: str, email: str, password: str, role: str):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.role = role

#methode zum debuggen, gibt in einfacher Darstellung aus
    def __repr__(self):
        return f"User(id={self.id}, name='{self.name}', email='{self.email}', role='{self.role}')"