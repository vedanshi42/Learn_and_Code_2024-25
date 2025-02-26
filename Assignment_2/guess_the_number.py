import random


def is_valid_number(user_input):
    if user_input.isdigit() and 1 <= int(user_input) <= 100:
        return True
    return False


def get_user_input():
    user_input = input("Guess a number between 1 and 100: ")
    while not is_valid_number(user_input):
        user_input = input("Invalid input. Please enter a number between 1 and 100: ")
    return int(user_input)


def compare_guessed_number(guessed_number, target_number):
    if guessed_number < target_number:
        print("Too low. Guess again.")
    elif guessed_number > target_number:
        print("Too high. Guess again.")
    else:
        print("Congratulations! You guessed it correctly.")


def main():
    system_generated_number = random.randint(1, 100)
    guessed_correctly = False
    guessed_number = get_user_input()
    attempts = 0

    while not guessed_correctly:
        if guessed_number != system_generated_number:
            compare_guessed_number(guessed_number, system_generated_number)
            attempts += 1
            guessed_number = int(input("Guess again: "))
        else:
            print(f"You guessed it in {attempts} guesses!")
            guessed_correctly = True


main()
