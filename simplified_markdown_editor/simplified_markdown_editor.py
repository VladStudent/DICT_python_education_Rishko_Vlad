formatters = [
    "plain",
    "bold",
    "italic",
    "header",
    "link",
    "inline-code",
    "ordered-list",
    "unordered-list",
    "new-line"
]

special_commands = ["!help", "!done"]

markdown = ""


def plain():
    return input("Text: ")


def bold():
    text = input("Text: ")
    return f"**{text}**"


def italic():
    text = input("Text: ")
    return f"*{text}*"


def inline_code():
    text = input("Text: ")
    return f"`{text}`"


def link():
    label = input("Label: ")
    url = input("URL: ")
    return f"[{label}]({url})"


def header():
    while True:
        level = int(input("Level: "))
        if 1 <= level <= 6:
            break
        else:
            print("The level should be within the range of 1 to 6")

    text = input("Text: ")
    return f"{'#' * level} {text}\n"


def new_line():
    return "\n"


def ordered_list():
    result = ""
    while True:
        rows = int(input("Number of rows: "))
        if rows > 0:
            break
        else:
            print("The number of rows should be greater than zero")

    for i in range(1, rows + 1):
        text = input(f"Row #{i}: ")
        result += f"{i}. {text}\n"

    return result


def unordered_list():
    result = ""

    while True:
        rows = int(input("Number of rows: "))
        if rows > 0:
            break
        else:
            print("The number of rows should be greater than zero")

    for i in range(1, rows + 1):
        text = input(f"Row #{i}: ")
        result += f"* {text}\n"

    return result


while True:
    command = input("Choose a formatter: ")

    if command == "!help":
        print("Available formatters:",
              " ".join(formatters))
        print("Special commands:",
              " ".join(special_commands))

    elif command == "!done":
        with open("output.md", "w") as file:
            file.write(markdown)

        print("Bye!")
        break

    elif command not in formatters:
        print("Unknown formatting type or command")

    else:
        if command == "plain":
            markdown += plain()

        elif command == "bold":
            markdown += bold()

        elif command == "italic":
            markdown += italic()

        elif command == "inline-code":
            markdown += inline_code()

        elif command == "link":
            markdown += link()

        elif command == "header":
            markdown += header()

        elif command == "new-line":
            markdown += new_line()

        elif command == "ordered-list":
            markdown += ordered_list()

        elif command == "unordered-list":
            markdown += unordered_list()

        print(markdown)