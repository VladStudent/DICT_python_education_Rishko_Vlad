import random
import string

def play_game():
    words = ["python", "java", "javascript", "php"]
    word = random.choice(words)
    hidden = ["-"] * len(word)
    guessed = set()
    lives = 8

    print("".join(hidden))

    while lives > 0:
        letter = input("Input a letter: > ")

        if len(letter) != 1:
            print("You should input a single letter")
            print("".join(hidden))
            continue

        if letter not in string.ascii_lowercase:
            print("Please enter a lowercase English letter")
            print("".join(hidden))
            continue

        if letter in guessed:
            print("You've already guessed this letter")
            print("".join(hidden))
            continue

        guessed.add(letter)

        if letter in word:
            updated = False
            for i in range(len(word)):
                if word[i] == letter:
                    hidden[i] = letter
                    updated = True

            if not updated:
                print("No improvements")
                lives -= 1
        else:
            print("That letter doesn't appear in the word")
            lives -= 1

        print("".join(hidden))

        if "-" not in hidden:
            print("You guessed the word!")
            print("You survived!")
            return

    print("You lost!")

print("HANGMAN")

while True:
    command = input('Type "play" to play the game,\n"exit" to quit: > ')
    if command == "play":
        play_game()
    elif command == "exit":
        break
