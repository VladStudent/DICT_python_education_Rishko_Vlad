board = ["_"] * 9
current = "X"

def print_grid():
    print("---------")
    print("|", board[0], board[1], board[2], "|")
    print("|", board[3], board[4], board[5], "|")
    print("|", board[6], board[7], board[8], "|")
    print("---------")

def check_winner(symbol):
    combos = [
        (0,1,2),(3,4,5),(6,7,8),
        (0,3,6),(1,4,7),(2,5,8),
        (0,4,8),(2,4,6)
    ]
    return any(board[a] == board[b] == board[c] == symbol for a,b,c in combos)

print_grid()

while True:
    coords = input("Enter the coordinates: ").split()

    if not all(c.isdigit() for c in coords):
        print("You should enter numbers!")
        continue

    x, y = map(int, coords)

    if x < 1 or x > 3 or y < 1 or y > 3:
        print("Coordinates should be from 1 to 3!")
        continue

    idx = (x - 1) * 3 + (y - 1)

    if board[idx] != "_":
        print("This cell is occupied! Choose another one!")
        continue

    board[idx] = current
    print_grid()

    if check_winner(current):
        print(f"{current} wins")
        break

    if "_" not in board:
        print("Draw")
        break

    current = "O" if current == "X" else "X"
