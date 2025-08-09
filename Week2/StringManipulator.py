# NOTE:
# The __init__ method is helpful because it automatically initialises object attributes
# when the object is created, we don’t need to call a separate method like set_text().
# This makes the code cleaner, reduces the risk of forgetting initialisation,
# and ensures the object is always ready to use after creation.
class StringManipulator:

    def set_text(self, text):
        self.text = text

    def find_character(self, char):
        return self.text.find(char)
    
    def print_length(self):
        print("Length of string:", len(self.text))

    def convert_to_uppercase(self):
        print("Uppercase string:", self.text.upper())

def main():
    name = StringManipulator()
    name.set_text("example")

    result = name.find_character("x")
    print("Index of char: ", result)

    name.print_length()
    name.convert_to_uppercase()

if __name__ == "__main__":
    main()