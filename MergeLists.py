'''
Title: Merge Lists
Author: Caitlin Hartig
Date: 12/8/22

This program uses a function called "merge" that takes two already sorted lists of possibly different lengths, and merges them together into a single sorted list.
The list is sorted via the sort method.

Tools Utilized: random, functions, lists, conditionals
'''

def main():
    print('Welcome to the program that merges together and sorts 2 lists!' '\n')

    length1 = input('Enter the length of list 1:') # User enters the length of list 1
    length2 = input('Enter the length of list 2:') # User enters the length of list 2

    if length1.isdigit() and length2.isdigit(): # Checks to see if both lengths are numbers
        if float(length1) and float(length2) % 1 != 0: # Checks to see if both lengths are integers
            print('Error! Please enter an integer.') # If the number is not an integer, an error message is printed.
        else:
            length1 = int(length1)
            length2 = int(length2)

            list1 = [] # This list will store a first list of randomly generated values
            list2 = [] # This list will store a second list of randomly generated values
    
            random_list(length1, list1) # The function "random_list" is called to create list 1 of length1
            random_list(length2, list2) # The function "random_list" is called to create list 2 of length2
            merge(list1, list2) # The function "merge" is called to merge together the two lists
    else:
        print('Error! Please enter a numeric integer.') # If the numbers are not integers, an error message is printed

def random_list(length, list):
    '''
    Function -- random_list
        Creates a random number list of a length determined by the user.
    Parameters:
        length -- the length determined by the user
        list -- an empty list to store the random numbers
    Returns a list of a length defined by the user with random numbers.
    '''
    from random import randint

    for i in range(length): # For any given length, a random list is generated for that length and stored in any given list
        list.append(randint(1,100))
    # print(list)
    list.sort() # The list is sorted
    print(list)

def merge(list1, list2):
    '''
    Function -- merge
        Takes two pre-existing lists of possibly different lengths, merges them together, and sorts the list.
    Parameters:
        list1 -- a first list of numbers
        list2 -- a second list of numbers
    Returns a new list containing all elements of list1 and list2, sorted.
    '''
    new_list = list1 + list2 # The two lists are merged together
    # print(new_list)
    new_list.sort() # The two lists are sorted
    print(new_list) # The final list is printed

main()