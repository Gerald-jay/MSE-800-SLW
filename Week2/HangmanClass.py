import random
import string

class HangmanClass:
    def __init__(self, words=None, lives=5):
        self.words = words if words else ["python", "game", "live", "life", "word"]
        self.lives = lives
        self.word = ""
        self.word_letters = set()
        self.guessed_letters = set()

    def pick_word(self):
        #Pick a random word form the list.
        self.word = random.choice(self.words)
        self.word_letters = set(self.word)
        self.guessed_letters = set()

    def display_progress(self):
        return " ".join([ch if ch in self.guessed_letters else "_" for ch in self.word]) 
    
    def paly(self):
        self.pick_word()

        print("Let's get started...")
        print("You have", self.lives, "lives")
        print("Word letters:", self.word_letters)
        print(self.display_progress())

        lives_life = self.lives

        while lives_life > 0 and len(self.word_letters) > 0:
            if len(self.word_letters) == len(self.guessed_letters): break
            guess = input("\nGuess a letter: ").lower().strip()

            if len(guess) != 1 or guess not in string.ascii_lowercase:
                print("Plese input One letter")
                continue

            if guess in self.guessed_letters:
                print("You already guessed")
                continue

            if guess in self.word_letters:
                self.guessed_letters.add(guess)
                print("Good guessed:", self.display_progress())
            else:
                lives_life -= 1
                if(lives_life == 0): break
                print(f"Wrong. Lives left:{lives_life}")
                print(self.display_progress())

        if lives_life > 0:
            print("YOU WIN. The word was:", self.word)
        else:
            print("GAME OVER. The word was:", self.word)
            return
    
if __name__ == "__main__":
    game = HangmanClass()
    game.paly()