'''
Title: Time Difference Calculator
Author: Caitlin Hartig
Date: 12/8/22

Purpose: This program calculates the difference in the number of minutes between one time and another.
Input:   Two distinct times, input in hh:mm am/pm format. Ex) 06:56 am
Output:  The difference, in minutes, between the two times. Ex) 27 minutes
Tools Utilized: Loops, conditionals, exception handling, functions
'''

def main():
    case = input('Would you like to calculate the distance between two times? Enter "Yes" to continue.')
    while case == 'Yes':
        first_time = input('Enter the first time (hh:mm am/pm):')               # Input - this is time #1
        second_time = input('Enter the second time (hh:mm am/pm):')             # Input - this is time #2

        hour1 = time_convert(first_time)                                        # Hours are converted into 24-hour format via the time_convert function
        hour2 = time_convert(second_time)

        try: # Checks to see if the times were entered in the correct format
            minutes1 = int(first_time[3:6])
            minutes2 = int(second_time[3:6])
        except:
            print('Error! Please enter valid minutes in format hh:mm am/pm')
        else:
            result = time_difference(hour1, hour2, minutes1, minutes2)          # The time difference is calculated via the time_difference function
            print(f'The difference is {result} minutes.')                       # Output - the time difference in minutes is printed
        
        case = input('Would you like to calculate the distance between two times? Enter "Yes" to continue.')

def time_convert(time):
    '''
    Function:   time_convert -- converts a time from 12-hour to 24-hour format
    Parameters: time -- the time to be converted
    Returns:    converted time
    '''
    try: # Checks to see if the times were entered in the correct format
        hour = int(time[0:2])
    except:
        print('Error! Please enter valid hour in format hh:mm am/pm')

    TIME_LOWER_12 = 1 # 1 is the lowest hour in 12-hour time
    TIME_UPPER_12 = 12 # 12 is the highest hour in 12-hour time
    TIME_CONVERT = 12 # 12 is the factor to convert from 12-hour time to 24-hour time  
    TIME_LOWER_24 = 0 # 0 is the lowest hour in 24-hour time

    if time[-2:] == 'pm': # If the time is in 'pm', 12 is added to convert to 24-hour time
        if TIME_LOWER_12 <= hour < TIME_UPPER_12:
            hour += TIME_CONVERT
            return hour
        else:
            return hour
    if time[-2:] == 'am':
        if hour == TIME_UPPER_12: # If the time is in 'am' but the hour is 12, it is converted to 0
            hour = TIME_LOWER_24
            return hour
        else:
            return hour

def time_difference(hour1, hour2, minutes1, minutes2):
    '''
    Function: time_difference -- calculates the difference in minutes between two times
    Parameters: hour1 -- the hour from the first time
                hour2 -- the hour from the second time
                minutes1 -- the minutes from the first time
                minutes2 -- the minutes from the second time
    Returns:    The time difference in minutes between the two times.
    '''
 
    TIME_LOWER_HOUR = 0 # 0 is the lowest possible value for the hour
    TIME_UPPER_HOUR = 24 # There are 24 hours in 24-hour time
    CONVERSION = 60 # There are 60 minutes in 1 hour
    TIME_LOWER_MINUTE = 0 # 0 is the lowest possible value for the minute
    TIME_UPPER_MINUTE = 60 # There are 60 minutes in 1 hour
    
    difference_hours = hour2 - hour1
    if difference_hours < TIME_LOWER_HOUR: # If the difference in hours is less than 0, 24 is added so that it is in range
        difference_hours += TIME_UPPER_HOUR
    difference_hours *= CONVERSION # The time difference in hours is converted into minutes
    #print(difference_hours)

    difference_minutes = minutes2 - minutes1
    if difference_minutes < TIME_LOWER_MINUTE: # If the difference in minutes is less than 0, 60 is added so that it is in range
        difference_minutes += TIME_UPPER_MINUTE
    #print(difference_minutes)

    if minutes1 > minutes2: # If the minutes from the first hour are higher than the minutes from the second hour, 60 is subtracted so as not to include a false hour result
        difference_hours -= TIME_UPPER_MINUTE
    #print(difference_hours)

    difference = difference_hours + difference_minutes # The difference is calculated in minutes
    return difference

if __name__ == '__main__':
    main()