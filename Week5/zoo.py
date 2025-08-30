class Color:
    def __init__(self, name):
        self.name = name

    def get_color(self):
        return self.name


class TransparentColor(Color):
    def __init__(self, name, transparency):
        super().__init__(name)
        self.transparency = transparency

    #override the parent cass method
    def get_color(self):
        return f"Color: {self.name}, TransparentColor:{self.transparency}%"

class Animal:
    def __init__(self, species, color: Color):
        self.species = species
        self.color = color

    def get_species(self):
        return self.species
    
def main():
    color = Color("Grayish-Black")
    elephant = Animal("Elephant", color)
    print(f"Animal: {elephant.get_species()}, Color: {elephant.color.get_color()}")

    transparent_color = TransparentColor("Brown", 65)
    kiwi = Animal("Kiwi", transparent_color)
    print(f"Animal: {kiwi.get_species()}, Color: {kiwi.color.get_color()}")

if __name__ == "__main__":
    main()


