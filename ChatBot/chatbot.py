def greet():
    bot_name = "VladBot"
    birth_year = "2025"
    print(f"Hello! My name is {bot_name}.")
    print(f"I was created in {birth_year}.")

def ask_name():
    print("Please, remind me your name.")
    name = input()
    print(f"What a great name you have, {name}!")

def guess_age():
    print("Let me guess your age.")
    print("Enter remainders of dividing your age by 3, 5 and 7.")
    r3 = int(input())
    r5 = int(input())
    r7 = int(input())
    age = (r3 * 70 + r5 * 21 + r7 * 15) % 105
    print(f"Your age is {age}; that's a good time to start programming!")

def count_numbers():
    print("Now I will prove to you that I can count to any number you want.")
    num = int(input())
    for i in range(num + 1):
        print(f"{i} !")

def test():
    print("Let's test your programming knowledge.")
    print("Why do we use methods?")
    print("1. To repeat a statement multiple times.")
    print("2. To decompose a program into several small subroutines.")
    print("3. To determine the execution time of a program.")
    print("4. To interrupt the execution of a program.")

    while True:
        ans = input()
        if ans == "2":
            break
        print("Please, try again.")

    print("Completed, have a nice day!")
    print("Congratulations, have a nice day!")


greet()
ask_name()
guess_age()
count_numbers()
test()
