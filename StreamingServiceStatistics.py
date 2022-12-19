'''
Title: Streaming Service Statistics
Author: Caitlin Hartig
Date: 12/8/22

Purpose: This program can be utilized by a marketing agency to make a telephone survey of the viewing audience to sample the popularity of a particular online streaming service
            that offers a wide variety of award-winning TV shows, movies, anime, and documentaries. The program can be implemented to collect data for multiple streaming services.
Input:  In each call made by the marketing agency, the age, residency status, and usage of the viewer are recorded as inputs.
Output: 1. Total number of people called, number of people who use the streaming service regularly, and percentage of those who used the service regularly.
        2. A table showing the percentages of those who use the streaming service regularly according to residency status and age.
Tools Utilized: Loops, counters, exception handling
'''

def main():

    case = input('Would you like to input information for a streaming service? Enter "Yes" to enter.')

    while case == "Yes":
        
        START_VALUE = 0                       # Counters are all set to 0 to start
        count_people = START_VALUE            # Tracks the total number of people called in the survey
        total_age = START_VALUE               # Tracks the total number of people whose ages were counted for the calculations
        under_25 = START_VALUE                # Tracks the total number of people called in the survey who are under age 25
        over_25 = START_VALUE                 # Tracks the total number of people called in the survey who are age 25 or older
        total_residency = START_VALUE         # Tracks the total number of people whose residency status was counted for the calculations
        local_under_25 = START_VALUE          # Tracks the total number of people called in the survey who are both local and under age 25
        local_over_25 = START_VALUE           # Tracks the total number of people called in the survey who are both local and age 25 or older
        foreigner_under_25 = START_VALUE      # Tracks the total number of people called in the survey who are both foreign and under age 25
        foreigner_over_25 = START_VALUE       # Tracks the total number of people called in the survey who are both foreign and age 25 or older
        count_stream = START_VALUE            # Tracks the total number of people called in the survey who use the streaming service regularly
        AGE_BRACKET = 25                      # We are interested in which users are under age 25 or are age 25 and older
        AGE_LOWER = 1                         # Lower limit of age range for people called in this survey
        AGE_UPPER = 120                       # Upper limit of age range for people called in this survey

        case_program = input('Would you like to input information for a person? Enter "Yes" to enter.')

        while case_program == "Yes":
            count_people += 1

            case_age = "Yes"
            while case_age == "Yes":
                age = input("What is this person's age? Must be in range 1-120.")

                try: # Converts the user age to an integer
                    age = int(age)
                except:
                    print('Error! Please enter a numeric digit for the age.')
                else:
                    if age < AGE_LOWER or age > AGE_UPPER: # Checks to make sure that the age entered is in the specified age range
                        print('Error! Please enter a valid age in range 1-120.')
                    else: # Age counters are updated according to survey input: total age, age under 25, and age 25 and over
                        total_age += 1
                        if age < AGE_BRACKET:
                            under_25 += 1
                        else:
                            over_25 += 1
                        break
            
            case_residency = "Yes"
            while case_residency == "Yes":
                residency = input("What is this person's residency status? Enter 'L' for Local or 'F' for Foreigner")
                residency = residency.upper()
                lst_residency = ['L', 'F']
                if residency not in lst_residency: # Checks to make sure the residency was input as specified
                        print('Error! Please enter either "L" for Local or "F" for Foreigner')  
                else: # Residency counters are updated according to both residency and age classifications: total residency, local under 25, local 25 and over, foreign under 25, foreign 25 and over
                    total_residency += 1
                    if age < AGE_BRACKET:
                        if residency == 'L':
                            local_under_25 += 1
                        else:
                            foreigner_under_25 += 1
                    else:
                        if residency == 'L':
                            local_over_25 += 1
                        else:
                            foreigner_over_25 += 1                    
                    break

            case_regular = "Yes"
            while case_regular == "Yes":
                regular = input("Does this person use the streaming service regularly? Enter 'Y' for Yes or 'N' for No\n")
                regular = regular.upper()
                lst_regular = ['Y', 'N']
                if regular not in lst_regular: # Checks to make sure the streaming status was input as specified
                    print("Error! Please enter 'Y' for Yes or 'N' for No") 
                else:
                    regular.upper()
                    if regular == 'Y':
                        count_stream += 1 # Number of people who regularly use the service is updated
                    else: # If the person does not regularly use the streaming service, the counters must be subtracted so as not to include false data
                        total_age -= 1
                        total_residency -= 1
                        if age < AGE_BRACKET:
                            under_25 -= 1
                            if residency == 'L':
                                local_under_25 -= 1
                            else:
                                foreigner_under_25 -= 1
                        else:
                            over_25 -= 1
                            if residency == 'L':
                                local_over_25 -= 1
                            else:
                                foreigner_over_25 -= 1
                    break

            case_program = input("Do you want to enter another person's details? Enter 'Yes' to enter.")

        print('The total number of people called = ', count_people)                                     # Output 1 - total number of people called
        print('The total number of people who use the streaming service regularly = ', count_stream)    # Output 1 - total number of people who use the streaming service regularly
        
        PERCENT = 100 # We are looking for a percentage, so results need to be multiplied by 100

        if count_people != 0 and total_age != 0:
            percentage = count_stream / count_people * PERCENT                                                  # Output 1 - percentage of people who use the streaming service regularly
            print(f'The percentage of those who use the streaming service regularly = {percentage:.0f}%', end='\n\n')

            # Ages are calculated for the final table:
            total_under_25 = under_25 / total_age * PERCENT
            total_over_25 = over_25 / total_age * PERCENT
            total_sum = total_under_25 + total_over_25

            # Residency is calculated for the final table based on age demographics:
            total_local_under_25 = local_under_25 / total_residency * PERCENT
            total_local_over_25 = local_over_25 / total_residency * PERCENT
            total_foreigner_under_25 = foreigner_under_25 / total_residency * PERCENT
            total_foreigner_over_25 = foreigner_over_25 / total_residency * PERCENT
            sum_local = total_local_under_25 + total_local_over_25
            sum_foreigner = total_foreigner_under_25 + total_foreigner_over_25

            # Output 2 - the results are printed in the final table:
            print('Residency', '% Under25', '% 25 or Over', '% Total', sep='     ', end='\n')
            print(f'Local            {total_local_under_25:.0f}            {total_local_over_25:.0f}              {sum_local:.0f}', end='\n')
            print(f'Foreigner        {total_foreigner_under_25:.0f}            {total_foreigner_over_25:.0f}              {sum_foreigner:.0f}', end='\n')
            print(f'Total            {total_under_25:.0f}            {total_over_25:.0f}              {total_sum:.0f}', end='\n')

        else:
            print(f'The percentage of those who use the streaming service regularly = 0%', end='\n\n')

            print('Residency', '% Under25', '% 25 or Over', '% Total', sep='     ', end='\n')
            print(f'Local            0            0              0', end='\n')
            print(f'Foreigner        0            0              0', end='\n')
            print(f'Total            0            0              0', end='\n')

        case = input('Do you want to input information for a different program? Enter "Yes" to enter.')

main()