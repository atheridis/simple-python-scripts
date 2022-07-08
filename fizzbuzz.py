def read(text, tp, conditions, failtext=None):
    """Example:\n
read("firsttext", int, lambda x: x < 10, "lasttext")"""
    inp = input(text)
    while True:
        try:
            inp = tp(inp)
        except:
            pass
        else:
            if conditions(inp):
                break
        if failtext:
            inp = input(failtext)
        else:
            inp = input(text)
    return inp

def fizzbuzz(dic={"fizz": 3, "buzz": 5}):
    n = int(input("Insert the maximum value to play fizzbuzz: "))

    for i in range(1, n + 1):
        word = ""
        for d in dic:
            word += d if i % dic[d] == 0 else ""
        word = i if not word else word
        print(word)


def userdefined_fizzbuzz():
    dic = {}
    print("Please insert fizzbuzz words and multiples.")

    while True:
        number = read(
            "Please enter a number greater than 1, \
or enter 0 to finish your inputs: ", int, lambda x: x >= 0)

#         while True:
#             number = input(
#                 "Please enter a number greater than 1, \
# or enter 0 to finish your inputs: ")
#             try:
#                 val = int(number)
#                 if val >= 0:
#                     break
#             except ValueError:
#                 pass
#         number = int(number)
        if number == 0:
            break
        word = input("Please enter your word: ")
        dic.update({word: number})

    fizzbuzz(dic)


if __name__ == "__main__":
    userdefined_fizzbuzz()
