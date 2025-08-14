class UserInformation:
    def __init__(self, name, age, address):
        self.name = name
        self.age = age
        self.address = address

    def input_information(self):
        self.name = input("Please input your name:")
        self.age = int(input("Please input your age:"))
        self.address = input("Please input your address")
        self.personal_details()

    def personal_details(self):
        personals = [self.name, self.age, self.address]
        return personals
    
    
        