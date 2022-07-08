import random


def generalised_monty_hall():
    MIN_DOORS = 3

    doors = input("How many doors do you want? \nNumber of Doors: ")
    while True:
        try:
            doors = int(doors)
        except:
            pass
        else:
            if doors >= MIN_DOORS:
                break
        doors = input(
            f"\nPlease choose a number larger than {MIN_DOORS - 1}\
\nNumber of Doors: ")

    cars = input("\nHow many cars do you want? \nNumber of Cars: ")
    while True:
        try:
            cars = int(cars)
        except:
            pass
        else:
            if 0 < cars < doors - 1:
                break
        cars = input(
            f"\nPlease choose a number between 1 and {doors - 2}\
\nNumber of Cars: ")

    goats = doors - cars

    choices = input(
        "\nHow many doors would you like to choose?\nNumber of Choices: ")
    while True:
        try:
            choices = int(choices)
        except:
            pass
        else:
            if 0 < choices < goats:
                break
        choices = input(
            f"\nPlease choose a number between 1 and {goats - 1}\
\nNumber of Choices: ")

    opened = input(
        "\nHow many doors do you want the presenter to open \
before you change your doors?\
\nNumber of Doors to be Opened: ")
    while True:
        try:
            opened = int(opened)
        except:
            pass
        else:
            if 0 <= opened < doors - choices - cars + 1:
                break
        opened = input(
            f"\nPlease choose a number between 0 and {doors - choices - cars}\
\nNumber of Doors to be Opened: ")

    closed = doors - opened

    changes = input(
        "\nHow many doors would you like to swap after the presenter opens the doors?\
\nNumber of Swaps: ")
    while True:
        try:
            changes = int(changes)
        except:
            pass
        else:
            if 0 <= changes <= min(choices, doors - choices - opened):
                break
        changes = input(
            f"\nPlease choose a number between 0 and \
{min(choices, doors - choices - opened)}\
\nNumber of Swaps: ")

    MAX_WIN = min(cars, choices)
    win = [0] * (MAX_WIN + 1)

    trial = 0
    trials = 100_000

    while trial < trials:
        trial += 1

        _goats = random.sample(range(doors), goats)

        _choices = random.sample(range(doors), choices)

        _opened = random.sample(
            [n for n in _goats if n not in _choices], opened)

        _changes = random.sample(
            [n for n in range(doors)
             if n not in (*_opened, *_choices)], changes)

        _choices = random.sample(_choices, len(_choices) - len(_changes))

        _choices.extend(_changes)

        _doors = [True] * doors
        for goat in _goats:
            _doors[goat] = False

        cars = 0
        for choice in _choices:
            if _doors[choice]:
                cars += 1
        win[cars] += 1

    print("")
    for i in range(len(win)):
        print(f"{i}/{MAX_WIN} : {round(win[i] / trials * 100,3)}%")


if __name__ == "__main__":
    generalised_monty_hall()
