class CoffeeMachine:
    def __init__(self):
        self.water = 400
        self.milk = 540
        self.beans = 120
        self.cups = 9
        self.money = 550


        self.state = "main"

        self.recipes = {
            "1": (250, 0, 16, 4),    # espresso
            "2": (350, 75, 20, 7),   # latte
            "3": (200, 100, 12, 6),  # cappuccino
        }

    def print_prompt(self):
        if self.state == "main":
            print("Write action (buy, fill, take, remaining, exit):")
        elif self.state == "buy":
            print("What do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino, back – to main menu:")
        elif self.state == "fill_water":
            print("Write how many ml of water do you want to add:")
        elif self.state == "fill_milk":
            print("Write how many ml of milk do you want to add:")
        elif self.state == "fill_beans":
            print("Write how many grams of coffee beans do you want to add:")
        elif self.state == "fill_cups":
            print("Write how many disposable cups of coffee do you want to add:")

    def remaining(self):
        print("The coffee machine has:")
        print(f"{self.water} of water")
        print(f"{self.milk} of milk")
        print(f"{self.beans} of coffee beans")
        print(f"{self.cups} of disposable cups")
        print(f"{self.money} of money")

    def can_make(self, w, m, b):
        if self.water < w:
            return False, "water"
        if self.milk < m:
            return False, "milk"
        if self.beans < b:
            return False, "coffee beans"
        if self.cups < 1:
            return False, "disposable cups"
        return True, ""

    def make_coffee(self, choice):
        w, m, b, price = self.recipes[choice]
        ok, missing = self.can_make(w, m, b)
        if not ok:
            print(f"Sorry, not enough {missing}!")
            return

        print("I have enough resources, making you a coffee!")
        self.water -= w
        self.milk -= m
        self.beans -= b
        self.cups -= 1
        self.money += price

    def process(self, command: str) -> bool:
        command = command.strip()

        if self.state == "main":
            if command == "exit":
                return False
            if command == "remaining":
                self.remaining()
            elif command == "take":
                print(f"I gave you {self.money}")
                self.money = 0
            elif command == "buy":
                self.state = "buy"
            elif command == "fill":
                self.state = "fill_water"
            return True

        if self.state == "buy":
            if command == "back":
                self.state = "main"
                return True
            if command in self.recipes:
                self.make_coffee(command)
            self.state = "main"
            return True

        if self.state == "fill_water":
            self.water += int(command)
            self.state = "fill_milk"
            return True

        if self.state == "fill_milk":
            self.milk += int(command)
            self.state = "fill_beans"
            return True

        if self.state == "fill_beans":
            self.beans += int(command)
            self.state = "fill_cups"
            return True

        if self.state == "fill_cups":
            self.cups += int(command)
            self.state = "main"
            return True

        return True


def main():
    machine = CoffeeMachine()
    while True:
        machine.print_prompt()
        user_input = input()
        if not machine.process(user_input):
            break


if __name__ == "__main__":
    main()
