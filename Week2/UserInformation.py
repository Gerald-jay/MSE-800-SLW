class UserInformation:

    def input_information(self):
        self.name = input("Please input your name: ")
        age_input = input("Please input your age: ")
        self.check_age(age_input)
        self.address = input("Please input your address: ")
        self.personal_details()

    def check_age(self, age_input):
        while(not age_input.strip().isdigit()):
            age_input = input("Please input your age number:")
        self.age = int(age_input)

    def personal_details(self):
        self.personals = [self.name, self.age, self.address]
    
    def print_details(self):
        self.personal_details()
        print(f"The details is: name: {self.personals[0]}, age: {self.personals[1]}, address: {self.personals[2]}")
        
    def year_add(self):
        years = input("\nHow many years do you want to add to your age? ")
        while(not years.strip().isdigit()):
            years = input("Please input your age number:")
        self.personals[1] += int(years)
        print(f"\nAfter {years} years, {self.personals[0]} will be {self.personals[1]} years old and live at {self.personals[2]}.")

if __name__ == "__main__":
    userInfo = UserInformation()
    userInfo.input_information()
    userInfo.print_details()
    userInfo.year_add()
