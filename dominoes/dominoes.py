import random


def create_domino_set():
    """Створює повний набір з 28 унікальних кістянок від [0,0] до [6,6]."""
    return [[i, j] for i in range(7) for j in range(i, 7)]


def distribute_pieces():
    """Розподіляє 28 кістянок: 14 у резерв, по 7 комп'ютеру та гравцю."""
    deck = create_domino_set()
    random.shuffle(deck)

    stock = deck[:14]
    computer = deck[14:21]
    player = deck[21:28]
    return stock, computer, player


def determine_start(computer, player):
    """
    Знаходить найбільший дубль серед гравців.
    Повертає: (стартова_кістка, статус_гравця, оновлений_комп, оновлений_гравець)
    """
    while True:
        max_comp_double = -1
        max_play_double = -1


        for piece in computer:
            if piece[0] == piece[1] and piece[0] > max_comp_double:
                max_comp_double = piece[0]


        for piece in player:
            if piece[0] == piece[1] and piece[0] > max_play_double:
                max_play_double = piece[0]


        if max_comp_double > max_play_double and max_comp_double != -1:
            start_piece = [max_comp_double, max_comp_double]
            computer.remove(start_piece)
            return start_piece, "player", computer, player

        elif max_play_double > max_comp_double and max_play_double != -1:
            start_piece = [max_play_double, max_play_double]
            player.remove(start_piece)
            return start_piece, "computer", computer, player

        else:
            stock, computer, player = distribute_pieces()


def display_field(stock, computer, player, snake):
    """Виводить ігрове поле згідно з вимогами форматування."""
    print("=" * 70)
    print(f"Stock size: {len(stock)}")
    print(f"Computer pieces: {len(computer)}\n")

    if len(snake) > 6:
        print(f"{snake[0]}{snake[1]}{snake[2]}...{snake[-3]}{snake[-2]}{snake[-1]}")
    else:
        print("".join(str(p) for p in snake))
    print()

    print("Your pieces:")
    for idx, piece in enumerate(player, start=1):
        print(f"{idx}:{piece}")
    print()



def is_move_legal(piece, side, snake):
    """Перевіряє, чи підходить кістка до обраного боку змійки."""
    if side == "left":
        target_num = snake[0][0]
        return piece[0] == target_num or piece[1] == target_num
    elif side == "right":
        target_num = snake[-1][1]
        return piece[0] == target_num or piece[1] == target_num
    return False


def format_and_place_piece(piece, side, snake):
    """Розворачує кістку правильним боком і додає в змійку."""
    if side == "left":
        target_num = snake[0][0]

        if piece[1] != target_num:
            piece = [piece[1], piece[0]]
        snake.insert(0, piece)
    elif side == "right":
        target_num = snake[-1][1]

        if piece[0] != target_num:
            piece = [piece[1], piece[0]]
        snake.append(piece)


def computer_ai_move(computer, snake):
    """Алгоритм підрахунку балів «рідкості» та вибору ходу для комп'ютера."""
    counts = {i: 0 for i in range(7)}
    for p in computer + snake:
        counts[p[0]] += 1
        counts[p[1]] += 1

    scored_pieces = []
    for piece in computer:
        score = counts[piece[0]] + counts[piece[1]]
        scored_pieces.append((score, piece))

    scored_pieces.sort(key=lambda x: x[0], reverse=True)

    for _, piece in scored_pieces:
        if is_move_legal(piece, "right", snake):
            return piece, "right"
        elif is_move_legal(piece, "left", snake):
            return piece, "left"

    return 0, None



def check_game_over(stock, computer, player, snake):
    """Перевіряє, чи закінчилась гра. Повертає True та статус переможця або False."""
    if len(player) == 0:
        print("Status: The game is over. You won!")
        return True
    if len(computer) == 0:
        print("Status: The game is over. The computer won!")
        return True

    if snake[0][0] == snake[-1][1]:
        num = snake[0][0]
        count = sum(piece.count(num) for piece in snake)
        if count >= 8:
            print("Status: The game is over. It's a draw!")
            return True

    return False



def main():
    stock, computer, player = distribute_pieces()
    start_piece, status, computer, player = determine_start(computer, player)
    snake = [start_piece]

    while True:
        display_field(stock, computer, player, snake)

        if check_game_over(stock, computer, player, snake):
            break

        if status == "player":
            print("Status: It's your turn to make a move. Enter your command.")
            try:
                command = input("> ").strip()

                move = int(command)


                if abs(move) > len(player):
                    print("Invalid input. Please try again.")
                    continue

                if move == 0:

                    if stock:
                        player.append(stock.pop())
                    status = "computer"
                else:
                    side = "right" if move > 0 else "left"
                    chosen_piece = player[abs(move) - 1]


                    if is_move_legal(chosen_piece, side, snake):
                        format_and_place_piece(chosen_piece, side, snake)
                        player.remove(chosen_piece)
                        status = "computer"
                    else:
                        print("Illegal move. Please try again.")


            except ValueError:
                print("Invalid input. Please try again.")

        elif status == "computer":
            input("Status: Computer is about to make a move. Press Enter to continue...\n> ")

            chosen_piece, side = computer_ai_move(computer, snake)

            if chosen_piece == 0:
                if stock:
                    computer.append(stock.pop())
            else:
                format_and_place_piece(chosen_piece, side, snake)
                computer.remove(chosen_piece)

            status = "player"


if __name__ == "__main__":
    main()