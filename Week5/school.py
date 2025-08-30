class School:
    def __init__(self, student_id, name, age):
        self.student_id = student_id
        self._name = name
        self.__age = age

    def get_age(self):
        return self.__age
    
    def set_age(self, new_age):
        if new_age > 0:
            self.__age = new_age
    
def main():
    s = School("S123", "Eason", 18)
    print("Student ID:", s.student_id)

    print("Name:", s._name)

    print("age:", s.get_age())

    s.set_age(20)
    print("New age:", s.get_age())

if __name__ == "__main__":
    main()