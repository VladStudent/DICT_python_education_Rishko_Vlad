import os
import random


def load_rating(name):
    """Зчитує початковий рейтинг користувача з файлу rating.txt."""
    if not os.path.exists("rating.txt"):
        return 0
    with open("rating.txt", "r", encoding="utf-8") as file:
        for line in file:
            parts = line.split()
            if parts and parts[0] == name:
                return int(parts[1])
    return 0


def determine_winner(user_choice, comp_choice, options):
    """Визначає результат гри на основі алгоритму зсуву списку."""
    if user_choice == comp_choice:
        return "draw"

    idx = options.index(user_choice)
    shifted_options = options[idx + 1 :] + options[:idx]

    half_size = len(shifted_options) // 2
    beaten_by = shifted_options[:half_size]

    if comp_choice in beaten_by:
        return "lose"
    else:
        return "win"


def main():
    name = input("Enter your name: ")
    print(f"Hello, {name}")

    rating = load_rating(name)

    options_input = input()
    if options_input.strip() == "":
        options = ["rock", "paper", "scissors"]
    else:
        options = [opt.strip() for opt in options_input.split(",")]

    print("Okay, let's start")

    while True:
        user_input = input().strip()

        if user_input == "!exit":
            print("Bye!")
            break

        if user_input == "!rating":
            print(f"Your rating: {rating}")
            continue

        if user_input not in options:
            print("Invalid input")
            continue

        comp_choice = random.choice(options)
        result = determine_winner(user_input, comp_choice, options)

        if result == "draw":
            print(f"There is a draw ({comp_choice})")
            rating += 50
        elif result == "lose":
            print(f"Sorry, but the computer chose {comp_choice}")
        elif result == "win":
            print(f"Well done. The computer chose {comp_choice} and failed")
            rating += 100


if __name__ == "__main__":
    main()