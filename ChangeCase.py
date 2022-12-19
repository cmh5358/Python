'''
Title: Change Case
Author: Caitlin Hartig
Date: 12/8/22

This program uses a function called "change_case". When given a string, the function returns the string with each uppercase letter replaced by a lowercase letter, and vice-versa.

Tools Utilized: strings, functions, loops, conditionals
'''

def main():
    print('Welcome to the program that changes the case of the characters in your string!' '\n')

    string = input('Enter a string:') # User enters a string
    if string.isalpha():
        change_case(string) # The function is called with the string as an argument
    else:
        print('Error! Please enter a character string with no numbers.')

def change_case(string):
    '''
    Function -- change_case
        Takes a string and replaces all the uppercase letters with lowercase letters, and vice-versa.
    Parameters:
        string -- a string entered by the user
    Returns the string with each uppercase letter replaced with a lowercase letter, and vice-versa.
    '''
    result = "" # Empty string is created as a placeholder

    for i in range(0,len(string)): # The for loop goes through all the letters in the string
        if string[i].isupper(): # If the letter is uppercase, it is converted to lowercase and added to the string
            result = result + string[i].lower()
        else:
            result = result + string[i].upper() # Otherwise, the letter is converted to uppercase and added to the string

    print(result)

main()