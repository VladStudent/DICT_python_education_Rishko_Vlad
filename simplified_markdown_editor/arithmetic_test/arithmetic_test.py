import random


def get_level():
    """Запит та валідація рівня складності."""
    while True:
        print("Which level do you want? Enter a number:")
        print("1 - simple operations with numbers 2-9")
        print("2 - integral squares of 11-29")
        choice = input("> ").strip()

        if choice in ["1", "2"]:
            return int(choice)
        else:
            print("Incorrect format.")


def generate_task(level):
    """Генерація завдання та повернення (текст_завдання, правильна_відповідь)."""
    if level == 1:
        num1 = random.randint(2, 9)
        num2 = random.randint(2, 9)
        operation = random.choice(["+", "-", "*"])
        task_str = f"{num1} {operation} {num2}"

        if operation == "+":
            correct_ans = num1 + num2
        elif operation == "-":
            correct_ans = num1 - num2
        else:
            correct_ans = num1 * num2

        return task_str, correct_ans
    else:
        num = random.randint(11, 29)
        task_str = f"{num}"
        correct_ans = num ** 2
        return task_str, correct_ans


def get_user_answer(task_str):
    """Запит відповіді користувача з обробкою винятків ValueError."""
    while True:
        print(task_str)
        user_input = input("> ").strip()
        try:
            return int(user_input)
        except ValueError:
            print("Incorrect format.")


def save_result(mark, level):
    """Збереження результатів у файл results.txt."""
    levels_desc = {
        1: "simple operations with numbers 2-9",
        2: "integral squares of 11-29"
    }

    name = input("What is your name?\n> ").strip()

    with open("results.txt", "a", encoding="utf-8") as f:
        f.write(f"{name}: {mark}/5 in level {level} ({levels_desc[level]}).\n")

    print('The results are saved in "results.txt".')


def main():
    level = get_level()
    correct_count = 0
    total_tasks = 5

    for _ in range(total_tasks):
        task_str, correct_ans = generate_task(level)
        user_ans = get_user_answer(task_str)

        if user_ans == correct_ans:
            print("Right!")
            correct_count += 1
        else:
            print("Wrong!")

    print(f"Your mark is {correct_count}/{total_tasks}.")

    save_choice = input("Would you like to save the result? Enter yes or no.\n> ").strip().lower()
    if save_choice in ["yes", "y"]:
        save_result(correct_count, level)


if __name__ == "__main__":
    main()