from random import random


def flip_coin():
    if random() > 0.5:
        return "Heads"
    return "Tails"


print(flip_coin())
