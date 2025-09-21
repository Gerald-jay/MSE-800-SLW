class Person:
    def __init__(self, name, address, age, ID):
        self.name = name
        self.address = address
        self.age = age
        self.ID = ID

    def greet(self):
        print(f"Person is Name:{self.name}, Age:{self.age}")
