import random

random_number = random.randint(1, 10)  # numbers 1 - 10
guess = None

while True:
    guess = input("Pick a number from 1 to 10: ")
    guess = int(guess)
    if guess < random_number:
        print("Too Low!")
    elif guess > random_number:
        print("Too High!")
    else:
        print("You Won!!!")
        play_again = input("Do you want to play again? (y/n) ")
        if play_again == "y":
            random_number = random.randint(1, 10)  # numbers 1 - 10
            guess = None
        else:
            print("Thank you for playing!")
            break
