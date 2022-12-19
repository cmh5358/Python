'''
Title: State Capital Quiz
Author: Caitlin Hartig
Date: 12/8/22

This program contains a dictionary using the U.S. states as keys, and their capitals as values.
The program then randomly quizzes the user by displaying the name of a state and asking the user to enter that state's capital.
The program keeps track of the number of correct and incorrect responses.

Tools Utilized: dictionary, loops, conditionals
'''

def main():
    print('Welcome to the program that quizzes you on state capitals!' '\n')

    # This dictionary contains states and their corresponding capitals.
    state_capital = {'Alabama':'Montgomery', 'Alaska':'Juneau', 'Arizona':'Phoenix', 'Arkansas':'Little Rock', 'California':'Sacramento', 'Colorado':'Denver', \
                    'Connecticut':'Hartford', 'Delaware':'Dover', 'Florida':'Tallahassee', 'Georgia':'Atlanta', 'Hawaii':'Honolulu', 'Idaho':'Boise', 'Illinois':'Springfield', \
                    'Indiana':'Indianapolis', 'Iowa':'Des Moines', 'Kansas':'Topeka', 'Kentucky':'Frankfort', 'Louisiana':'Baton Rouge', 'Maine':'Augusta', 'Maryland':'Annapolis', 'Massachusetts':'Boston', \
                    'Michigan':'Lansing', 'Minnesota':'Saint Paul', 'Mississippi':'Jackson', 'Missouri':'Jefferson City', 'Montana':'Helena', 'Nebraska':'Lincoln', 'Nevada':'Carson City', \
                    'New Hampshire':'Concord', 'New Jersey':'Trenton', 'New Mexico':'Santa Fe', 'New York':'Albany', 'North Carolina':'Raleigh', 'North Dakota':'Bismarck', 'Ohio':'Columbus', \
                    'Oklahoma':'Oklahoma City', 'Oregon':'Salem', 'Pennsylvania':'Harrisburg', 'Rhode Island':'Providence', 'South Carolina':'Columbia', 'South Dakota':'Pierre', \
                    'Tennessee':'Nashville', 'Texas':'Austin', 'Utah':'Salt Lake City', 'Vermont':'Montpelier', 'Virginia':'Richmond', 'Washington':'Olympia', 'West Virginia':'Charleston', \
                    'Wisconsin':'Madison', 'Wyoming':'Cheyenne'}

    case = input('Would you like to play Guess the Capital? Enter "Yes" to play:')
    correct = 0 # The number of correct guesses is counted
    incorrect = 0 # The number of incorrect guesses is counted

    while case == 'Yes':
        if len(list(state_capital.keys())) != 0: # The program continues only if there are still remaining items in the dictionary
            option = list(state_capital.popitem()) # A random option is obtained from the dictionary
            state = option[0] # The state is obtained from the random option
            capital = option[1] # The capital is obtained from the random option
            print('What is the capital of ', state, sep='', end='?\n')
            guess = input('Enter your guess:') # The user enters a guess for the capital
            if guess == capital: # If the user guesses correcty, the tally for correct guesses is increased by 1
                correct += 1
                print('Correct! Your current score is:', correct)
                case = input('Would you like to keep playing? Enter "Yes" to continue:')
            else: # If the user guesses incorrecty, the tally for incorrect guesses is increased by 1
                incorrect += 1
                print('Incorrect! Your current score is:', correct)
                case = input('Would you like to keep playing? Enter "Yes" to continue:')
        else:
            break
    print('Your number of correct responses is:', correct) # The number of correct guesses is printed
    print('Your number of incorrect responses is:', incorrect) # The number of incorrect guesses is printed

main()