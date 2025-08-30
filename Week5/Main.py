
class Person:
    def __init__(self, name, address, age, ID):
        self.name = name
        self.address = address
        self.age = age
        self.ID = ID

class Student(Person):
    def __init__(self, name, address, age, ID, record):
        super().__init__(name, address, age, ID)
        self.record = record

class Academic(Person):
    def __init__(self, name, address, age, ID, tax, salary):
        super().__init__(name, address, age, ID)
        self.tax = tax
        self.salary = salary

class Staff(Academic):
    def __init__(self, name, address, age, ID, tax, salary, pay):
        super().__init__(name, address, age, ID, tax, salary)
        self.pay = pay

if __name__ == "__main__":
    s = Student("Eason", "Wellington", 18, "S123", "Excellent")
    a = Academic("Dr. Bob", "Auckland", 45, "A101", "TX001", 90000)
    st = Staff("Carol", "Christchurch", 35, "ST55", "TX002", 35, 500)
