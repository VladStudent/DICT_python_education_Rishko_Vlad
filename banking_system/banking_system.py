import sqlite3
import random

conn = sqlite3.connect("card.s3db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS card (
    id INTEGER PRIMARY KEY,
    number TEXT,
    pin TEXT,
    balance INTEGER DEFAULT 0
);
""")

conn.commit()


def generate_checksum(number):
    digits = [int(x) for x in number]

    for i in range(len(digits)):
        if i % 2 == 0:
            digits[i] *= 2
            if digits[i] > 9:
                digits[i] -= 9

    checksum = (10 - (sum(digits) % 10)) % 10
    return str(checksum)


def check_luhn(card_number):
    digits = [int(x) for x in card_number]

    checksum = digits.pop()

    for i in range(len(digits)):
        if i % 2 == 0:
            digits[i] *= 2
            if digits[i] > 9:
                digits[i] -= 9

    return (sum(digits) + checksum) % 10 == 0


def create_account():
    while True:
        account_identifier = str(random.randint(100000000, 999999999))
        card_without_checksum = "400000" + account_identifier

        checksum = generate_checksum(card_without_checksum)

        card_number = card_without_checksum + checksum

        cur.execute("SELECT number FROM card WHERE number = ?", (card_number,))
        if not cur.fetchone():
            break

    pin = str(random.randint(0, 9999)).zfill(4)

    cur.execute(
        "INSERT INTO card (number, pin) VALUES (?, ?)",
        (card_number, pin)
    )

    conn.commit()

    print("\nYour card has been created")
    print("Your card number:")
    print(card_number)
    print("Your card PIN:")
    print(pin)


def log_into_account():
    print("\nEnter your card number:")
    card_number = input()

    cur.execute("SELECT * FROM card WHERE number = ?", (card_number,))
    account = cur.fetchone()

    if not account:
        print("\nWrong card number!")
        return

    print("Enter your PIN:")
    pin = input()

    if pin != account[2]:
        print("\nWrong PIN!")
        return

    print("\nYou have successfully logged in!")

    account_menu(account)


def account_menu(account):
    while True:
        print("""
1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit
""")

        choice = input()

        if choice == "1":
            cur.execute(
                "SELECT balance FROM card WHERE number = ?",
                (account[1],)
            )

            balance = cur.fetchone()[0]

            print(f"\nBalance: {balance}")

        elif choice == "2":
            print("\nEnter income:")
            income = int(input())

            cur.execute(
                "UPDATE card SET balance = balance + ? WHERE number = ?",
                (income, account[1])
            )

            conn.commit()

            print("Income was added!")

        elif choice == "3":
            print("\nTransfer")
            print("Enter card number:")
            target = input()

            if target == account[1]:
                print("\nYou can't transfer money to the same account!")
                continue

            if not check_luhn(target):
                print("\nProbably you made a mistake in the card number. Please try again!")
                continue

            cur.execute(
                "SELECT * FROM card WHERE number = ?",
                (target,)
            )

            target_account = cur.fetchone()

            if not target_account:
                print("\nSuch a card does not exist.")
                continue

            print("Enter how much money you want to transfer:")
            amount = int(input())

            cur.execute(
                "SELECT balance FROM card WHERE number = ?",
                (account[1],)
            )

            balance = cur.fetchone()[0]

            if balance < amount:
                print("\nNot enough money!")
                continue

            cur.execute(
                "UPDATE card SET balance = balance - ? WHERE number = ?",
                (amount, account[1])
            )

            cur.execute(
                "UPDATE card SET balance = balance + ? WHERE number = ?",
                (amount, target)
            )

            conn.commit()

            print("\nSuccess!")

        elif choice == "4":
            cur.execute(
                "DELETE FROM card WHERE number = ?",
                (account[1],)
            )

            conn.commit()

            print("\nThe account has been closed!")
            break

        elif choice == "5":
            print("\nYou have successfully logged out!")
            break

        elif choice == "0":
            print("\nBye!")
            exit()


while True:
    print("""
1. Create an account
2. Log into account
0. Exit
""")

    choice = input()

    if choice == "1":
        create_account()

    elif choice == "2":
        log_into_account()

    elif choice == "0":
        print("\nBye!")
        break

conn.close()