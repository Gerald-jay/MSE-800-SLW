import random
import string

WORDS = ["python", "game", "live", "life", "word"]

def pick_word():
    return random.choice(WORDS)

def display_progerss(word, guessed):
    return " ".join([ch if ch in guessed else "_" for ch in word])

def play():
    word = pick_word()
    word_letters = set(word)
    guessed_letters = set()
    lives = 5

    print("Let's get started...")
    print("You have", lives, "lives")
    #print("word: ", word)
    print("word_letters: ", word_letters)
    print(display_progerss(word, guessed_letters))

    if lives == 0:
        return "GAME OVER"
    while lives > 0 and len(word_letters) > 0:
        if len(word_letters) == len(guessed_letters): break
        guess = input("\nGuess a letter:").lower().strip()
        if len(guess) != 1 or guess not in string.ascii_lowercase:
            print("Plese input One letter")
            continue

        if guess in guessed_letters:
            print("You already guessed")
            continue

        if guess in word_letters:
            guessed_letters.add(guess)
            #print("The word:", " ".join(sorted(guessed_letters)))
            print("Good guessed:", display_progerss(word, guessed_letters))
        else:
            lives -= 1
            if(lives == 0): break
            print(f"Wrong. Lives left:{lives}")
            print(display_progerss(word, guessed_letters))

    if lives > 0:
        print("YOU WIN. The word was:", word)
    else:
        print("GAME OVER. The word was:", word)
        return

if __name__ == "__main__":
    ans = play() 
    