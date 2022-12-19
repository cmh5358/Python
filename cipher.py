'''
Title: Cipher
Author: Caitlin Hartig
Date: 12/8/22

This program takes a message as input and both encrypts it and decrypts it using the Caesar Cipher.

Tools Utilized: string, functions, strings, exception handling, conditionals, dictionary, loops
'''

import string

def main():
    plaintext = input('What message would you like to encrypt?') # User enters a message
    key = input('What key would you like to use? Enter a numeric integer in range 1-26:') # User enters a key to use for the encryption / decryption

    ciphertext = encrypt(plaintext, key)
    print('The encrypted message is:', ciphertext) # The encrypted message is printed

    decrypted = decrypt(ciphertext, key)
    print('The decrypted message is:', decrypted) # The decrypted message is printed

def input_test(message, key):
    '''
    Function -- input_test
        Tests the input message and the key. The program quits and enters an error message if it encounters an error.
    Parameters:
        message -- the message will be converted into uppercase, without spaces or punctuation
        key -- the key will be tested to see if it is an integer and is in the specified range
    Returns:
        message, key -- the modified message and the key
    '''
    message = message.upper() # Message is converted to uppercase
    message = message.strip() # White space is stripped from the message
    message = message.translate(str.maketrans('', '', string.punctuation)) # Punctuation is removed from the message
    message = message.replace(' ', '') # Spaces are removed from the message
    #print(message)

    try:
        key = int(key)
        ALPHABET_LETTERS = 26 # There are 26 letters in the alphabet
        ALPHABET_MIN = 1 # The first letter of the alphabet is assigned number 1
        if key < ALPHABET_MIN or key > ALPHABET_LETTERS: # If the key is not in range 1-26, the program quits
            quit()
        return message, key
    except: # An error message is printed if either the key is not a numeric integer, or the key is not in range 1-26
        print('Error! Please enter a valid numeric integer in range 1-26.')
        quit()

def encrypt(plaintext, key):
    '''
    Function -- encrypt
        Converts a plaintext message into ciphertext using a key.
    Parameters:
        plaintext -- the message to be encrypted
        key -- the conversion factor that will be added to each letter to convert each letter into a different letter
    Returns:
        ciphertext -- the encrypted message
    '''
    plaintext, key = input_test(plaintext, key) # The plaintext message is input into the input_test function

    alphabet = {'A':1, 'B':2, 'C':3, 'D':4, 'E':5, 'F':6, 'G':7, 'H':8, 'I':9, 'J':10, 'K':11, 'L':12, 'M':13, 'N':14, 'O':15, 'P':16, 'Q':17, 'R':18, 'S':19, \
                'T':20, 'U':21, 'V':22, 'W':23, 'X':24, 'Y':25, 'Z':26} # This dictionary holds all the letters of the alphabet and assigns each letter a number in order 1-26

    str = '' # This empty string will hold the encrypted message
    ALPHABET_LETTERS = 26 # There are 26 letters in the alphabet

    for letter in plaintext: # The key is added to each letter in the message
        value = alphabet.get(letter)
        value_new = value + key

        if value_new > ALPHABET_LETTERS: # If the new value for the letter is above 26, 26 is subtracted so that the new letter is in range 1-26
            value_new = value_new - ALPHABET_LETTERS

        alphabet_pairs = alphabet.items()
        for alphabet_pair in alphabet_pairs:
            if alphabet_pair[1] == value_new:
                str += alphabet_pair[0] # The letter associated with the new value is added to the string

    return str

def decrypt(ciphertext, key):
    '''
    Function -- decrypt
        Converts a ciphertext message into plaintext using a key.
    Parameters:
        ciphertext -- the message to be decrypted
        key -- the conversion factor that will be subtracted from each letter to convert each letter into a different letter
    Returns:
        plaintext -- the decrypted message
    '''

    ciphertext, key = input_test(ciphertext, key) # The ciphertext message is input through the input_test function

    alphabet = {'A':1, 'B':2, 'C':3, 'D':4, 'E':5, 'F':6, 'G':7, 'H':8, 'I':9, 'J':10, 'K':11, 'L':12, 'M':13, 'N':14, 'O':15, 'P':16, 'Q':17, 'R':18, 'S':19, \
                'T':20, 'U':21, 'V':22, 'W':23, 'X':24, 'Y':25, 'Z':26} # This dictionary holds all the letters of the alphabet and assigns each letter a number in order 1-26
    
    str = '' # This empty string will hold the decrypted message
    ALPHABET_LETTERS = 26 # There are 26 letters in the alphabet
    ALPHABET_MIN = 1 # The first letter of the alphabet is assigned number 1

    for letter in ciphertext: # The key is added to each letter in the message
        value = alphabet.get(letter)
        value_new = value - key

        if value_new < ALPHABET_MIN: # If the new value for the letter is below 1, 26 is added so that the new letter is in range 1-26
            value_new = value_new + ALPHABET_LETTERS

        alphabet_pairs = alphabet.items()
        for alphabet_pair in alphabet_pairs:
            if alphabet_pair[1] == value_new:
                str += alphabet_pair[0] # The letter associated with the new value is added to the string

    return str    

if __name__ == '__main__':
    main()