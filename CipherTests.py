'''
Title: Cipher Tests
Author: Caitlin Hartig
Date: 12/8/22

This program tests the cipher program.

Tools Utilized: functions, conditionals
'''

import cipher

def encrypt_tests(plaintext, key, expected):
    '''
    Function encrypt_tests
    Parameters: plaintext -- the message to be converted
                key -- the key used to encrypt the message
    Return -- true if actual == expected; false otherwise
    Does -- calls the encrypt function and compares actual vs expected to determine success
    '''
    print('Testing points', plaintext, key, sep=', ')
    actual_encrypt = cipher.encrypt(plaintext, key)
    if actual_encrypt == expected:
        return True

def run_encrypt_tests():
    '''
    Function run_encrypt_tests
    Parameters: none
    Returns: an int, number of tests that failed
    '''

    num_fail_encrypt = 0
    if (encrypt_tests('PROFJUMP', 3, 'SURIMXPS')): # test 1
        print('PASSED! :)')
    else:
        print('FAILED :(')
        num_fail_encrypt +=1

    num_fail_encrypt = 0
    if (encrypt_tests('CAITLIN', 3, 'FDLWOLQ')): # test 2
        print('PASSED! :)')
    else:
        print('FAILED :(')
        num_fail_encrypt +=1

    num_fail_encrypt = 0
    if (encrypt_tests('   Hello! My name, Caitlin, is. Awesome.   ', 3, 'KHOORPBQDPHFDLWOLQLVDZHVRPH')): # test 3
        print('PASSED! :)')
    else:
        print('FAILED :(')
        num_fail_encrypt +=1

    return num_fail_encrypt # The total of failed tests is returned

def decrypt_tests(ciphertext, key, expected):
    '''
    Function decrypt_tests
    Parameters: ciphertext -- the message to be decrypted
                key -- the key used to decrypt the message
    Return -- true if actual == expected; false otherwise
    Does -- calls the decrypt function and compares actual vs expected to determine success
    '''
    print('Testing points', ciphertext, key, sep=', ')
    actual_decrypt = cipher.decrypt(ciphertext, key)
    if actual_decrypt == expected:
        return True

def run_decrypt_tests():
    '''
    Function run_decrypt_tests
    Parameters: none
    Returns: an int, number of tests that failed
    '''

    num_fail_decrypt = 0
    if (decrypt_tests('SURIMXPS', 3, 'PROFJUMP')): # test 1
        print('PASSED! :)')
    else:
        print('FAILED :(')
        num_fail_decrypt +=1

    num_fail_decrypt = 0
    if (decrypt_tests('FDLWOLQ', 3, 'CAITLIN')): # test 2
        print('PASSED! :)')
    else:
        print('FAILED :(')
        num_fail_decrypt +=1

    num_fail_decrypt = 0
    if (decrypt_tests('  KHOORPB..QDP!%HFD*LWOLQLVDZHVRPH  ', 3, 'HELLOMYNAMECAITLINISAWESOME')): # test 3
        print('PASSED! :)')
    else:
        print('FAILED :(')
        num_fail_decrypt +=1

    return num_fail_decrypt # The total of failed tests is returned

def main():
    print('Testing Encryption Cipher:') # Failure diagnostics for Encryption Cipher tests are calculated and printed
    failures_encrypt = run_encrypt_tests()
    if failures_encrypt == 0:
        print('Everything passed. Great job functions!\n\n')
    else:
        print('Something went wrong. Go back and fix please.\n\n')

    print('Testing Decryption Cipher:') # Failure diagnostics for Decryption Cipher tests are calculated and printed
    failures_decrypt = run_decrypt_tests()
    if failures_decrypt == 0:
        print('Everything passed. Great job functions!\n\n')
    else:
        print('Something went wrong. Go back and fix please.\n\n')

if __name__ == '__main__':
    main()