'''
Title: Star Box
Author: Caitlin Hartig
Date: 12/8/22

This program uses a for loop to print a box of '*' in a height and width defined by the user.

Tools Utilized: For loops
'''

def main():
    print('Welcome to the program that prints a box of stars!' '\n')

    height = eval(input('How high should the box be?')) # The user inputs a value for the height
    width = eval(input('How wide should the box be?')) # The user inputs a value for the width

    for i in range(height): # This for loop prints a box of stars as defined by the user-input height and width
        print('*' * width)

main()