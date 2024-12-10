import random


def roll_dice(sides):
    dice_output = random.randint(1, sides)
    return dice_output


def dice():
    sides = 6
    rolling = True
    while rolling:
        quit_rolling = input("Ready to roll? Enter Q to Quit")
        if quit_rolling.lower() != "q":
            number_after_rolling = roll_dice(sides)
            print("You have rolled a", number_after_rolling)
        else:
            rolling = False


dice()


# Assignment 2: The below program is to guess the correct number between 1 to 100
def verify_number(input_number):
    if input_number.isdigit() and 1 <= int(input_number) <= 100:
        return True
    else:
        return False


def guess_the_number():
    generated_number = random.randint(1, 100)
    guessed_correctly = False
    guessed_number = input("Guess a number between 1 and 100:")
    number_of_guesses = 0
    while not guessed_correctly:
        if not verify_number(guessed_number):
            guessed_number = input("I won't count this one Please enter a number between 1 to 100")
            continue
        else:
            number_of_guesses += 1
            guessed_number = int(guessed_number)

        if guessed_number < generated_number:
            guessed_number = input("Too low. Guess again")
        elif guessed_number > generated_number:
            guessed_number = input("Too High. Guess again")
        else:
            print("You guessed it in", number_of_guesses, "guesses!")
            guessed_correctly = True


guess_the_number()

# Assignment 3: The below program is to check whether the number is Armstrong number or not


def check_Armstrong(input_number):
    # Initializing Sum and Number of Digits
    sum_of_digits = 0
    number_of_digits = 0

    # Calculating Number of individual digits
    number_to_check = input_number
    while number_to_check > 0:
        number_of_digits += 1
        number_to_check = number_to_check // 10

    # Finding Armstrong Number
    number_to_check = input_number
    for loop_counter in range(1, number_to_check + 1):
        remainder = number_to_check % 10
        sum_of_digits = sum_of_digits + (remainder ** number_of_digits)
        number_to_check //= 10
    return sum_of_digits


# End of Function

# User Input
input_number = int(input("\nPlease Enter the Number to Check for Armstrong: "))

if (input_number == check_Armstrong(input_number)):
    print("\n %d is Armstrong Number.\n" % input_number)
else:
    print("\n %d is Not a Armstrong Number.\n" % input_number)
