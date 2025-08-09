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