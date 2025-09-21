from person import Person

class Student(Person):
    def __init__(self, name, address, age, ID, record):
        super().__init__(name, address, age, ID)
        self.record = record

    def greet(self):
        print(f"Student is Name:{self.name}, Age:{self.age}, record:{self.record}")

if __name__ == "__main__":
    #p = Person("Li", "Auckland", "18", "T123")
    #print(f"Person is name:{p.name}, Age:{p.age}, address:{p.address}")

    s = Student("Eason", "Auckland", "11", "S123", "Excellent")
    s.greet()