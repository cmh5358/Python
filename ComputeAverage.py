'''
Title: Compute Average
Author: Caitlin Hartig
Date: 12/8/22

This program writes and then reads a file called numbers.txt that contains a series of integers.
This program displays the average of all the numbers stored in the file.

Tools Utilized: file handling, exception handling, lists, loops
'''

def main():
    print('Welcome to the program that displays the average of all the numbers stored in a file!' '\n')

    outfile = open('numbers.txt', 'w') # File numbers.txt is created and integers are added into it
    outfile.write('500\n')
    outfile.write('650\n')
    outfile.write('337\n')
    outfile.write('26')
    outfile.close()

    try:
        infile = open('numbers.txt', 'r') # The file is opened
        my_list = [] # This list will store the numbers from the file

        try:
            num = infile.readline() # The first number is read from the file, stripped empty space, and converted into integer
            num = int(num.rstrip())
            while num != '': # If a number is read from the file and converted into an integer, it is appended to the list
                my_list.append(num)
                print(num)
                num = int(infile.readline())
        except: # If the number is not an integer, an error message is printed
            print('Error! Not a valid number')
        finally:
            print(my_list)
            total = sum(my_list) # The sum of all the numbers is calculated
            count = len(my_list) # The count of all the numbers is calculated
            average = total / count # The average is calculated
            print('Out of', count, 'numbers, the total is', total, 'and the average is', average) # The average is printed

        infile.close
    except: # If the file is invalid, an error message is printed
        print('Error! Please enter a valid file.')

main()