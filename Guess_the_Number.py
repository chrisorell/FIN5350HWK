import random

def header(low_num, high_num):
    print ("\tWelcome to 'Guess My Number'!")
    print ("\tI'm thinking of a number between", low_num," and ",high_num, ".")
    print ("\tTry to outsmart the computer.\n")
    
def footer1(user_num, tries):
    print ("You lost")
    print ("It guessed you number! It was", user_num)
    print ("It took", tries, "tries!\n")
    print ("Press enter key to exit.")
    
def footer2(user_num):
    print ("Game over, you win!")
    print ("The computer didn't guess your number")
    print ("The number was", user_num)
    print ("Press enter key to exit.")

def main():
    
    user_num = 50
    low_num = 1
    high_num = 100
    tries = 0
    max_tries = 8
    
    header(low_num, high_num)
    
    comp_guess = random.randint(low_num, high_num)
    
    comp_guess
    
    while comp_guess != user_num & tries < max_tries:
        if comp_guess < user_num:
            low_num = comp_guess
            print ("Higher, computer guessed", comp_guess)
            comp_guess = random.randint(low_num, high_num)
        if comp_guess > user_num:
            high_num = comp_guess
            print ("Lower, computer guessed", comp_guess)
            comp_guess = random.randint(low_num, high_num)
        if comp_guess == user_num & tries < max_tries:
            footer1(user_num, tries)
            break
        if tries >= max_tries:
            footer2(user_num)
            break
        tries += 1
        
if __name__ == "__main__":
    main()