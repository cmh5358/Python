'''
Title: Display Information About a Student
Author: Caitlin Hartig
Date: 12/8/22

Purpose: This client program creates instances of the "Student" class. It then creates a menu option for the user:
            1. Quit program
            2. Add to a list information about a student through user input, to determine the student's grade.
            3. Output from the list all information about the students currently stored in the list, including their overall marks and final grades.
            4. Compute and output the average overall mark for students currently held in the list, without using pre-defined methods.
            5. Determine and display how many students obtained an overall mark equal to or above the average overall mark, and how many obtained an overall mark below the average overall mark.
            6. Display the distribution of grades awarded and provide a graphical representation of the same.
            7. Given a student ID number, view all details of the student with that number. Print an error message if the student is not found in the list.
            8. Given a student's first name and last name, view all details of that student. Print an error message if the student is not found in the list.
            9. Sort the list of student objects into ascending order of the students' ID numbers, and output the sorted list. Use your own sorting method. Analyze the time complexity of the algorithm.
            The menu loops around until the user selects Option 1 - Quit.
Input:  For each instance of a student object, input is: first name, last name, student ID number, birthdate, assignment 1 grade, assignment 2 grade, total lab grade, and final exam grade.
Output: 3. For each instance of a student object, the output is first name, last name, student ID number, birthdate, grade for assignment 1, grade for assignment 2, lab grade, final exam grade,
             overall mark, and final grade. Overall mark and final grade are not provided as inputs, but rather are calculated from within the program itself.
             In addition, the program notifies the user if a duplicate student has been entered by returning "True" if yes, or "False" if no.
        4. The average overall mark for students currently held in the list.
        5. Number of students who obtained an overall mark equal to or above the average overall mark, and number of students who obtained an overall mark below the average overall mark.
        6. The distribution of grades awarded and a graphical representation of the same.
        7. All details of a student when given their student ID number.
        8. All details of a student when given their first and last name.
        9. A sorted list of student objects in ascending order of their student ID numbers.
Tools Utilized: Object Oriented Programming, menu option, lists, strings, manual sort function, loops, conditionals, counters, exception handling, matplotlib
'''

def bubble_sort(lst): # The Bubble Sort function will be called in menu option 9 to sort the list. This algorithm has time complexity = n^2
    n = len(lst)
    for i in range(n):
        for j in range((i+1),n):
            if lst[i].get_student_ID() > lst[j].get_student_ID():
                lst[i], lst[j] = lst[j], lst[i]
    return lst

def main():

    import StudentClass
    import matplotlib.pyplot as plt

    global lst
    lst = [] # This list holds all students in the database. 4 students are hard-coded to begin with, so that the program runs even if the user does not input information for any more students.
    student1 = StudentClass.Student('Cathy', 'Hart', '4761', '29/12/1989', 98, 97, 10, 96)
    student2 = StudentClass.Student('Zifu', 'Long', '5761', '11/03/1999', 100, 99, 10, 98)
    student3 = StudentClass.Student('Lila', 'Hunter', '4143', '04/11/1990', 72, 79, 10, 60)
    student4 = StudentClass.Student('Astoria', 'Sharkish', '5221', '15/10/1990', 85, 87, 8, 88)

    lst.append(student1)
    lst.append(student2)
    lst.append(student3)
    lst.append(student4)

    # The average is calculated for the hard-coded students so that menu options 4-6 work even if the user does not input information for any more students.
    total = 0
    for i in range(len(lst)):
        total += lst[i].get_overall_mark()
    #print(total)

    length = len(lst)
    average = total / length
    #print(average)

    case_master = 'Yes'
    while case_master == 'Yes':

        print('Which menu option would you like to choose? \n \
            1. Quit \n \
            2. Enter information for a student and determine their final grade \n \
            3. Output the details of all students currently held in the database \n \
            4. Calculate the average overall mark for students currently held in the database \n \
            5. Determine and display how many students obtained an overall mark equal to or above, vs below, the average overall mark \n \
            6. Display the distribution of grades (number of HDs, Ds, etc) awarded, and show the display as a graph \n \
            7. Enter a student ID number, view all details of the student with that number \n \
            8. Enter a student name and view all details of the student with that name \n \
            9. Sort the database of students into ascending order based on their student ID number \n')

        lst_case = ['1', '2', '3', '4', '5', '6', '7', '8', '9'] # This list holds the numbers of all available menu options

        case = input('Enter choice:') # User chooses a menu option

        if case == lst_case[0]: # If selected, quits the program
            case_master = 'No'

        if case == lst_case[1]: # If selected, user inputs details of an instance of a student object
            case_student = input('2. Would you like to enter information for a student and determine their final grade? Enter "Yes" to input.')
        
            while case_student == 'Yes': # Ask today's date to be able to calculate age range for birth year later
                CURRENT_YEAR = 2022 # The current year is 2022. This is necessary to check that the user input birth year is in the correct range

                first_name = input("What is the student's first name?")
                last_name = input("What is the student's last name?")
                student_ID = input("What is the student's student ID number?")
                birthdate = input("What is the student's birthdate? dd/mm/yyyy")

                # Birthdate is checked that it is input in correct format as well as if the day, month, and year are in the correct range
                case_birthdate = 'N'

                while case_birthdate == 'N':
                    try:
                        day = int(birthdate[:2])
                        month = int(birthdate[3:5])
                        year = int(birthdate[-4:])
                        case_birthdate = 'Y'
                    except:
                        print('Error! Invalid format.')
                        birthdate = input("What is the student's birthdate? dd/mm/yyyy")
                        case_birthdate = 'N'
                    else:
                        LOWER_LIMIT = 1 # We don't want any numbers below 1 for day or month, or for (current year - birth year)
                        # These are the upper limits for day, month, and year:
                        UPPER_LIMIT_DAY = 31 # There are 31 days in a month
                        UPPER_LIMIT_MONTH = 12 # There are 12 months in a year
                        UPPER_LIMIT_AGE = 120 # To validate the year, an upper age limit of 120 is placed

                        if int(birthdate[:2]) < LOWER_LIMIT:
                            print('Error! Day must be in range 1-31.')
                            birthdate = input("What is the student's birthdate? dd/mm/yyyy")
                            case_birthdate = 'N'
                        if int(birthdate[:2]) > UPPER_LIMIT_DAY:
                            print('Error! Day must be in range 1-31.')
                            birthdate = input("What is the student's birthdate? dd/mm/yyyy")
                            case_birthdate = 'N'
                        if int(birthdate[3:5]) < LOWER_LIMIT:
                            print('Error! Month must be in range 1-12.')
                            birthdate = input("What is the student's birthdate? dd/mm/yyyy")
                            case_birthdate = 'N'
                        if int(birthdate[3:5]) > UPPER_LIMIT_MONTH:
                            print('Error! Month must be in range 1-12.')
                            birthdate = input("What is the student's birthdate? dd/mm/yyyy")
                            case_birthdate = 'N'
                        if (CURRENT_YEAR - int(year)) < LOWER_LIMIT:
                            print('Error! Age must be in range 1-120.')
                            birthdate = input("What is the student's birthdate? dd/mm/yyyy")
                            case_birthdate = 'N'
                        if (CURRENT_YEAR - int(year)) > UPPER_LIMIT_AGE:
                            print('Error! Age must be in range 1-120.')
                            birthdate = input("What is the student's birthdate? dd/mm/yyyy")
                            case_birthdate = 'N'

                # When grades are entered, they are checked that they are floating point numbers as well as in the correct range

                case_assignment1 = 'N'
                assignment1 = input('What grade did the student receive on Assignment 1?')

                # Assignment 1 grade must be in range 0-100
                UPPER_LIMIT_ASSIGNMENT1 = 100
                LOWER_LIMIT_ASSIGNMENT1 = 0

                while case_assignment1 == 'N':
                    try:
                        assignment1 = float(assignment1)
                        case_assignment1 = 'Y'
                    except:
                        print('Error! Please enter a numeric value for assignment 1.')
                        assignment1 = input('What grade did the student receive on Assignment 1?')
                        case_assignment1 = 'N'
                    else:
                        if assignment1 < LOWER_LIMIT_ASSIGNMENT1 or assignment1 > UPPER_LIMIT_ASSIGNMENT1:
                            print('Error! Grade must be in range 0-100.')
                            assignment1 = input('What grade did the student receive on Assignment 1?')
                            case_assignment1 = 'N'

                case_assignment2 = 'N'
                assignment2 = input('What grade did the student receive on Assignment 2?')

                # Assignment 2 grade must be in range 0-100
                UPPER_LIMIT_ASSIGNMENT2 = 100
                LOWER_LIMIT_ASSIGNMENT2 = 0

                while case_assignment2 == 'N':
                    try:
                        assignment2 = float(assignment2)
                        case_assignment2 = 'Y'
                    except:
                        print('Error! Please enter a numeric value for Assignment 2.')
                        assignment2 = input('What grade did the student receive on Assignment 2?')
                        case_assignment2 = 'N'
                    else:
                        if assignment2 < LOWER_LIMIT_ASSIGNMENT2 or assignment2 > UPPER_LIMIT_ASSIGNMENT2:
                            print('Error! Grade must be in range 0-100.')
                            assignment2 = input('What grade did the student receive on Assignment 2?')
                            case_assignment2 = 'N'

                case_lab = 'N'
                lab = input('What total grade did the student receive for all of their labs?')

                # Lab grade must be in range 0-10
                UPPER_LIMIT_LAB = 10
                LOWER_LIMIT_LAB = 0

                while case_lab == 'N':
                    try:
                        lab = float(lab)
                        case_lab = 'Y'
                    except:
                        print('Error! Please enter a numeric value for the total lab grade.')
                        lab = input('What total grade did the student receive for all of their labs?')
                        case_lab = 'N'
                    else:
                        if lab < LOWER_LIMIT_LAB or lab > UPPER_LIMIT_LAB:
                            print('Error! Grade must be in range 0-10.')
                            lab = input('What total grade did the student receive for all of their labs?')
                            case_lab = 'N'

                case_final_exam = 'N'
                final_exam = input('What grade did the student receive on their final exam?')

                # Final Exam grade must be in range 0-100
                UPPER_LIMIT_FINAL_EXAM = 100
                LOWER_LIMIT_FINAL_EXAM = 0

                while case_final_exam == 'N':
                    try:
                        final_exam = float(final_exam)
                        case_final_exam = 'Y'
                    except:
                        print('Error! Please enter a numeric value for the final exam grade.')
                        final_exam = input('What grade did the student receive on their final exam?')
                        case_final_exam = 'N'
                    else:
                        if final_exam < LOWER_LIMIT_FINAL_EXAM or final_exam > UPPER_LIMIT_FINAL_EXAM:
                            print('Error! Grade must be in range 0-100.')
                            final_exam = input('What grade did the student receive on their final exam?')
                            case_final_exam = 'N'

                student1 = StudentClass.Student(first_name, last_name, student_ID, birthdate, assignment1, assignment2, lab, final_exam) # An instance of the student class object is created

                # Check to see if the student is already in the database:

                isFound = False

                for student in lst:
                    result = student.equals(student1)
                    if result == True:
                        isFound = True
                
                if isFound == True:
                    print('Error - this student is a duplicate of another student already entered')
                else:
                    lst.append(student1)

                case_student = input('Would you like to enter information for another student? Enter "Yes" to input.')

        if case == lst_case[2]: # Prints the details of all students currently held in the list
            for i in range(len(lst)):
                print(lst[i])

        if case == lst_case[3]: # Computes the average overall mark for all students currently held in the list
            total = 0
            for i in range(len(lst)):
                total += lst[i].get_overall_mark() 
            #print(total)

            length = len(lst)
            average = total / length
            print('The average overall mark for students currently held in the database is', average)

        if case == lst_case[4]: # Determines how many students obtained an overall mark equal to or above the average overall mark, and how many obtained an overall mark below the average overall mark
            lst_average = [] # This list will hold the averages of all students in the list
            count_equals_above = 0 # Counts those with average equal to or above the overall mark. Set to 0 to start
            count_below = 0 # Counts those with average below the overall mark. Set to 0 to start
            for i in range(len(lst)):
                lst_average.append(lst[i].get_overall_mark())

            #print(lst_average)

            for element in lst_average:
                if element >= average:
                    count_equals_above += 1
                else:
                    count_below += 1

            print(f'{count_equals_above} is the number of students that obtained an overall mark equal to or above the average overall mark')
            print(f'{count_below} is the number of students that obtained an overall mark below the average overall mark')

        if case == lst_case[5]: # Shows the distribution of grades awarded and provides a graphical representation of the same
            lst_grade = [] # This list will hold the final grade of all students in the list
            for i in range(len(lst)):
                lst_grade.append(lst[i].get_final_grade())

            # print(lst_grade)

            # Counters for each grade are set to 0 to start
            count_HD = 0
            count_D = 0
            count_C = 0
            count_P = 0
            count_N = 0

            # These are the available letter grades:
            HIGHEST_GRADE = 'HD'
            SECOND_HIGHEST_GRADE = 'D'
            MIDDLE_GRADE = 'C'
            SECOND_LOWEST_GRADE = 'P'
            LOWEST_GRADE = 'N'

            for element in lst_grade:
                if element == HIGHEST_GRADE:
                    count_HD += 1
                elif element == SECOND_HIGHEST_GRADE:
                    count_D += 1
                elif element == MIDDLE_GRADE:
                    count_C += 1
                elif element == SECOND_LOWEST_GRADE:
                    count_P += 1
                elif element == LOWEST_GRADE:
                    count_N += 1

            # The distribution of all grades awarded is printed
            print('The number of HD grades is', count_HD)
            print('The number of D grades is', count_D)
            print('The number of C grades is', count_C)
            print('The number of P grades is', count_P)
            print('The number of N grades is', count_N)

            # The distribution of all grades awarded is displayed as a graph
            x_coords = [LOWEST_GRADE, SECOND_LOWEST_GRADE, MIDDLE_GRADE, SECOND_HIGHEST_GRADE, HIGHEST_GRADE]
            y_coords = [count_N, count_P, count_C, count_D, count_HD]
            #print(y_coords)
            
            plt.bar(x_coords, y_coords)
            plt.title('Distribution of Grades')
            plt.xlabel('Grade')
            plt.ylabel('Count')

            plt.xticks([0, 1, 2, 3, 4],
                        [LOWEST_GRADE, SECOND_LOWEST_GRADE, MIDDLE_GRADE, SECOND_HIGHEST_GRADE, HIGHEST_GRADE])

            plt.yticks([0, 5, 10, 15, 20],
                        [0, 5, 10, 15, 20])

            #plt.grid(True)
            plt.show()

        if case == lst_case[6]: # Given a student ID number, all details of the student with that number are displayed
            student_ID = input("Enter a student ID number:")

            isFound = False

            for i in range(len(lst)): # If the student is in the database, all details are printed
                if lst[i].get_student_ID() == student_ID:
                    isFound = True
                    print(lst[i])
            if isFound == False: # If the student is not in the database, an error is printed
                error = 'Error! Student with ID ' + student_ID + ' is not in the database'
                print(error)

        if case == lst_case[7]: # Given a student's first and last name, all details of the student with that name are displayed
            last_name = input("Enter a student's last name")
            first_name = input("Enter a student's first name")

            isFound = False

            for student in lst: # If the student is in the database, all details are printed
                if student.get_last_name() == last_name and student.get_first_name() == first_name:
                    isFound = True
                    print(student)
            if isFound == False: # If the student is not in the database, an error is printed
                error = 'Error! Student with name ' + first_name + ' ' + last_name + ' is not in the database'
                print(error)

        if case == lst_case[8]: # The student objects in the list are sorted in ascending order by student ID number, using the bubble sort function
            for i in range(len(lst)):
                bubble_sort(lst)
                print(lst[i])

        if case not in lst_case: # If the user does not select a valid menu option, an error is printed
            print('Error! Please select a valid menu option.')

main()