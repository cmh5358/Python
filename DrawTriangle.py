'''
Title: Draw Triangle
Author: Caitlin Hartig
Date: 12/8/22

This program uses Turtle to draw a triangle.

Tools Utilized: turtle, math
'''

def main():
    print('Welcome to the program that uses Turtle to draw a triangle!' '\n')

main()

import turtle
import math

turtle.dot()
turtle.forward(math.sqrt(2)*100)
turtle.dot()
turtle.setheading(135)
turtle.forward(100)
turtle.dot()
turtle.setheading(-135)
turtle.forward(100)
turtle.done()