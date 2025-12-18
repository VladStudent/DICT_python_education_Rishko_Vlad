import random

players = ["John", "Jack"]

# ----- INPUT PENCILS -----
while True:
    pencils = input("How many pencils would you like to use:\n")
    if not pencils.isdigit():
        print("The number of pencils should be numeric")
        continue
    pencils = int(pencils)
    if pencils <= 0:
        print("The number of pencils should be positive")
        continue
    break

# ----- INPUT FIRST PLAYER -----
while True:
    current_player = input(f"Who will be the first ({players[0]}, {players[1]}):\n")
    if current_player not in players:
        print(f"Choose between '{players[0]}' and '{players[1]}'")
        continue
    break

print("|" * pencils)

# ----- GAME LOOP -----
while pencils > 0:
    print(f"{current_player}'s turn:")

    if current_player == "Jack":
        if pencils == 1:
            take = 1
        elif pencils % 4 == 1:
            take = random.randint(1, min(3, pencils))
        else:
            take = (pencils - 1) % 4
        print(take)
    else:
        while True:
            take = input()
            if take not in ["1", "2", "3"]:
                print("Possible values: '1', '2' or '3'")
                continue
            take = int(take)
            if take > pencils:
                print("Too many pencils were taken")
                continue
            break

    pencils -= take

    if pencils == 0:
        winner = players[0] if current_player == players[1] else players[1]
        print(f"{winner} won!")
        break

    print("|" * pencils)
    current_player = players[0] if current_player == players[1] else players[1]
