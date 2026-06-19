import random

friends_count = int(input("Enter the number of friends joining (including you):\n> "))

if friends_count <= 0:
    print("No one is joining for the party")
else:
    friends = {}
    print("Enter the name of every friend (including you), each on a new line:")
    for _ in range(friends_count):
        friends[input("> ")] = 0

    total = float(input("Enter the total amount:\n> "))
    choice = input('Do you want to use the "Who is lucky?" feature? Write Yes/No:\n> ')

    if choice == "Yes":
        lucky = random.choice(list(friends.keys()))
        print(f"{lucky} is the lucky one!")

        share = round(total / (friends_count - 1), 2)
        for name in friends:
            friends[name] = 0 if name == lucky else share
    else:
        print("No one is going to be lucky")
        share = round(total / friends_count, 2)
        for name in friends:
            friends[name] = share

    print(friends)
