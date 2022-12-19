'''
Title: "Student" Class Object
Author: Caitlin Hartig
Date: 12/8/22

Purpose: This program creates a class "Student" and assigns attributes to it.
Input:   First name, last name, student ID number, birthdate, grade for assignment 1, grade for assignment 2, lab grade, final exam grade.
Output:  Prints the attributes of the Student class: first name, last name, student ID number, birthdate, grade for assignment 1, grade for assignment 2, lab grade, final exam grade,
             overall mark, and final grade. Overall mark and final grade are not provided as inputs, but rather are calculated from within the program itself.
             In addition, the program notifies the user if a duplicate student has been entered by returning "True" if yes, or "False" if no.
Tools Utilized: Object Oriented Programming, methods, functions, conditionals
'''

class Student:
    '''
    This class stores information about a student (first_name, last_name, student ID number, birthdate, assignment1 grade, assignment2 grade, total lab grade, and final exam grade).
    The overall mark and the final grade are not input, but are calculated from within the program itself, and displayed as output as attributes of the class.
    '''
    def __init__(self, first_name, last_name, student_ID, birthdate, assignment1, assignment2, lab, final_exam):
        '''
        This constructor initializes the attributes first_name, last_name, student_ID, birthdate, assignment1, assignment2, lab, final_exam, overall_mark, and final_grade to an object.
        '''
        self.__first_name = first_name
        self.__last_name = last_name
        self.__student_ID = student_ID
        self.__birthdate = birthdate
        self.__assignment1 = assignment1
        self.__assignment2 = assignment2
        self.__lab = lab
        self.__final_exam = final_exam
        self.__overall_mark = 0 # Overall mark is set to 0 to start
        self.__final_grade = '' # Final grade is set as an empty string to start

        self.calculate_overall_mark() # Overall mark is calculated
        self.calculate_final_grade() # Final grade is calculated

    def set_first_name(self, first_name):
        '''
        This is the mutator for the first name.
        '''
        self.__first_name = first_name

    def get_first_name(self):
        '''
        This is the accessor for the first name.
        '''
        return self.__first_name

    def set_last_name(self, last_name):
        '''
        This is the mutator for the last_name.
        '''
        self.__last_name = last_name

    def get_last_name(self):
        '''
        This is the accessor for the last_name.
        '''
        return self.__last_name

    def set_student_ID(self, student_ID):
        '''
        This is the mutator for the student ID number.
        '''
        self.__student_ID = student_ID

    def get_student_ID(self):
        '''
        This is the accessor for the student_ID.
        '''
        return self.__student_ID

    def set_birthdate(self, birthdate):
        '''
        This is the mutator for the birthdate.
        '''
        self.__birthdate = birthdate

    def get_birthdate(self):
        '''
        This is the accessor for the birthdate.
        '''
        return self.__birthdate

    def set_assignment1(self, assignment1):
        '''
        This is the mutator for the assignment1.
        '''
        self.__assignment1 = assignment1

    def get_assignment1(self):
        '''
        This is the accessor for the assignment1.
        '''
        return self.__assignment1

    def set_assignment2(self, assignment2):
        '''
        This is the mutator for the assignment2.
        '''
        self.__assignment2 = assignment2

    def get_assignment2(self):
        '''
        This is the accessor for the assignment2.
        '''
        return self.__assignment2

    def set_lab(self, lab):
        '''
        This is the mutator for the lab.
        '''
        self.__lab = lab

    def get_lab(self):
        '''
        This is the accessor for the total lab grade.
        '''
        return self.__lab

    def set_final_exam(self, final_exam):
        '''
        This is the mutator for the final_exam.
        '''
        self.__final_exam = final_exam

    def get_final_exam(self):
        '''
        This is the accessor for the final_exam.
        '''
        return self.__final_exam

    def get_overall_mark(self):
        '''
        This is the accessor for the overall mark.
        '''
        return self.__overall_mark

    def get_final_grade(self):
        '''
        This is the accessor for the final grade.
        '''
        return self.__final_grade

    def calculate_overall_mark(self):
        '''
        Function:   calculate_overall_mark -- calculate's a student's overall mark by calculating a weighted average from their grades on all assignments
        Parameters: self -- the instance of a student
        Returns:    nothing -- void function. Updates the overall mark to be equal to the newly calculated overall mark
        '''
        # The total marks for each assignment are as follows:
        TOTAL_ASSIGNMENT1 = 100
        TOTAL_ASSIGNMENT2 = 100
        TOTAL_LAB = 10
        TOTAL_FINAL_EXAM = 100

        # Grades for the above assignments are weighted as follows:
        WEIGHT_ASSIGNMENTS_SUM = 0.40 # The weight of the sum of Assignment 1 and Assignment 2 together
        WEIGHT_LAB = 0.10
        WEIGHT_FINAL_EXAM = 0.50

        PERCENTAGE = 100 # We are looking for a percentage, so need to multiply by 100

        # Overall Mark is calculated as follows:
        overall_mark = ((((self.__assignment1 + self.__assignment2) / (TOTAL_ASSIGNMENT1 + TOTAL_ASSIGNMENT2))) * WEIGHT_ASSIGNMENTS_SUM \
                    + (self.__lab / TOTAL_LAB) * WEIGHT_LAB \
                    + (self.__final_exam / TOTAL_FINAL_EXAM) * WEIGHT_FINAL_EXAM) \
                    * PERCENTAGE

        self.__overall_mark = overall_mark

    def calculate_final_grade(self):
        '''
        Function:   calculate_final_grade -- assigns a letter grade to the student based on their numerical overall mark
        Parameters: self -- the instance of a student
        Returns:    nothing -- void function. Updates the final grade to be equal to the newly calculated final grade
        '''
        overall_mark = self.__overall_mark

        # The lower limits of each letter grade are as follows:
        HD_LOWER = 80
        D_LOWER = 70
        C_LOWER = 60
        P_LOWER = 50
        # Below 'P' grade is an 'N' grade. Upper limit of 'N' is the same as the lower limit of 'P', which is equal to 50

        # Letter grades are assigned based on where the overall mark falls in comparison to the lower limits described above
        if overall_mark >= HD_LOWER:
            final_grade = 'HD'
        elif D_LOWER <= overall_mark < HD_LOWER:
            final_grade = 'D'
        elif C_LOWER <= overall_mark < D_LOWER:
            final_grade = 'C'
        elif P_LOWER <= overall_mark < C_LOWER:
            final_grade = 'P'
        elif overall_mark < P_LOWER:
            final_grade = 'N'

        self.__final_grade = final_grade

    def equals(self1, self2):
        '''
        Function:   equals -- compares attributes of one student instance to another student instance and determines if it is a duplicate student
        Parameters: self -- the instance of a student
        Returns:    "True" if the student is a duplicate; "False" if the student is not a duplicate
        '''
        # If a student's first name, last name, birthdate, and student ID number are all the same as another student's in the database, then "True" is returned to indicate a duplicate.
        if self1.__first_name == self2.__first_name:
            if self1.__last_name == self2.__last_name:
                if self1.__birthdate == self2.__birthdate:
                    if self1.__student_ID == self2.__student_ID:
                        return True
        else:
            return False

    def __str__(self):
        '''
        This prints the information for the class: first_name, last_name, student_ID, birthdate, assignment1, assignment2, lab, final_exam, overall_mark, final_grade.
        '''
        return f'First Name: {self.__first_name}\n' + \
               f'Last Name: {self.__last_name}\n' + \
               f'Student ID: {self.__student_ID}\n' + \
               f'Birthdate: {self.__birthdate}\n' + \
               f'Assignment 1 Grade: {self.__assignment1}\n' + \
               f'Assignment 2 Grade: {self.__assignment2}\n' + \
               f'Total Lab Grade: {self.__lab}\n' + \
               f'Final Exam Grade: {self.__final_exam}\n' + \
               f'Overall Mark: {self.__overall_mark}\n' + \
               f'Final Grade: {self.__final_grade}\n'