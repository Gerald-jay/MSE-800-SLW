
class LibraryItem:
    def __init__(self, title, author):
        self.__title = title
        self.__author = author
    
    def get_title(self):
        return self.__title
    
    def set_title(self, title):
        self.__title = title
    
    def get_author(self):
        return self.__author
    
    def set_author(self, author):
        self.__author = author

    def show_info(self):
        return{
            'title': self.get_title(),
            'author': self.get_author()
        }

class Book(LibraryItem):
    def __init__(self, title, author, species):
        super().__init__(title, author)
        self.__species = species

    def get_species(self):
        return self.__species
    
    def set_species(self, species):
        self.__species = species

    def show_info(self):
        print("=========")
        return{
            'title': self.get_title(),
            'author': self.get_author(),
            'species': self.get_species()
        }

class Magazine(LibraryItem):
    def __init__(self, title, author, issue_frequency):
        super().__init__(title, author)
        self.__issue_frequency = issue_frequency
    
    def get_issue_frequency(self):
        return self.__issue_frequency
    
    def set_issue_frequency(self, issue_frequency):
        self.__issue_frequency = issue_frequency

    def show_info(self):
        print("+++++")
        return{
            'title': self.get_title(),
            'author': self.get_author(),
            'issue_frequency': self.get_issue_frequency()
        }

class Library:
    def __init__(self):
        self.items = []

    def add_item(self, item: LibraryItem):
        self.items.append(item)

    def remove_item(self, item: LibraryItem):
        print("items size = ", self.items.__len__())
        if item in self.items:
            self.items.remove(item)

    def display_items(self):
        for item in self.items:
            item.show_info()

def main():
    book_1 = Book("Fluent Python", "Luciano Ramalho", "Python")
    magazine_1 = Magazine("North & South Magazine", "northandsouth", "Monthly")

    l = Library()
    l.add_item(book_1)
    l.add_item(magazine_1)

    l.display_items()

    l.remove_item(book_1)
    l.display_items()

if __name__ == "__main__":
    main()