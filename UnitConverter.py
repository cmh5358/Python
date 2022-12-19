'''
Title: Unit Converter
Author: Caitlin Hartig
Date: 12/8/22

Purpose: This program converts a value from unit of measurement to another.
            Options: distance (cm, m, km, in, ft, yd, mi), temperature (C, F), volume (l, cup, qt, gal), weight (oz, lb, ton, gr, kg, st)
Input:   Option; value to be converted; from units; to units
Output:  The value in the target unit

Tools Utilized: Menu option, conditionals, lists
'''

def main():
    print('What kind of unit would you like to convert:\n1 - distance\t(cm, m, km, in, ft, yd, mi)\n2 - temperature\t(C, F)\n' \
            '3 - volume\t(l, cup, qt, gal)\n4 - weight\t(oz, lb, ton, gr, kg, st)')
    
    case = input('Enter choice:') # User inputs their choice from the menu option

    if case == '1':
        value = float(input('Enter the value to be converted:')) # User enters a value to be converted
        from_units = input('Enter the abbreviation for the starting units:') # User enters the abbreviation for the starting units
        to_units = input('Enter the abbreviation for the target units:') # User enters the abbreviation for the target units
        unit_list = ['cm', 'm', 'km', 'in', 'ft', 'yd', 'mi']
        if from_units in unit_list and to_units in unit_list: # This if statement checks to see if the starting units and target units are valid for this selection
            result = distance(value, from_units, to_units) # The result is calculated from the function
            print(value, from_units, 'is equal to', result, to_units) # The resulting conversion is printed
        else:
            print('Error! Cannot convert', value, from_units, 'to', to_units) # If either the starting units or target units are invalid, an error message is printed

    elif case == '2':
        value = float(input('Enter the value to be converted:')) # User enters a value to be converted
        from_units = input('Enter the abbreviation for the starting units:') # User enters the abbreviation for the starting units
        to_units = input('Enter the abbreviation for the target units:') # User enters the abbreviation for the target units
        unit_list = ['C', 'F']
        if from_units in unit_list and to_units in unit_list: # This if statement checks to see if the starting units and target units are valid for this selection
            result = temperature(value, from_units, to_units) # The result is calculated from the function
            print(value, from_units, 'is equal to', result, to_units) # The resulting conversion is printed
        else:
            print('Error! Cannot convert', value, from_units, 'to', to_units) # If either the starting units or target units are invalid, an error message is printed

    elif case == '3':
        value = float(input('Enter the value to be converted:')) # User enters a value to be converted
        from_units = input('Enter the abbreviation for the starting units:') # User enters the abbreviation for the starting units
        to_units = input('Enter the abbreviation for the target units:') # User enters the abbreviation for the target units
        unit_list = ['l', 'cup', 'qt', 'gal']
        if from_units in unit_list and to_units in unit_list: # This if statement checks to see if the starting units and target units are valid for this selection
            result = volume(value, from_units, to_units) # The result is calculated from the function
            print(value, from_units, 'is equal to', result, to_units) # The resulting conversion is printed
        else:
            print('Error! Cannot convert', value, from_units, 'to', to_units) # If either the starting units or target units are invalid, an error message is printed

    elif case == '4':
        value = float(input('Enter the value to be converted:')) # User enters a value to be converted
        from_units = input('Enter the abbreviation for the starting units:') # User enters the abbreviation for the starting units
        to_units = input('Enter the abbreviation for the target units:') # User enters the abbreviation for the target units
        unit_list = ['oz', 'lb', 'ton', 'gr', 'kg', 'st']
        if from_units in unit_list and to_units in unit_list: # This if statement checks to see if the starting units and target units are valid for this selection
            result = weight(value, from_units, to_units) # The result is calculated from the function
            print(value, from_units, 'is equal to', result, to_units) # The resulting conversion is printed
        else:
            print('Error! Cannot convert', value, from_units, 'to', to_units) # If either the starting units or target units are invalid, an error message is printed

    else:
        print('Error! Please enter a valid number for your choice.') # If the user does not enter a valid selection, an error message is printed

def distance(value, from_units, to_units):
    '''
    Function: distance -- convert distances
    Parameters: value -- the distance to be converted
                from_units -- the abbreviation of the starting distance
                to_units -- the abbreviation of the target distance
    Returns converted distance, or
            -1 if the from_units or to_units are invalid
    '''
    CENTIMETER = 100 # Conversion numbers based on 1 meter are input as constants for conversions
    KILOMETER = 0.001
    INCH = 39.370078740157
    FOOT = 3.2808398950131
    YARD = 1.0936132983377
    MILE = 0.000621371
    METER = 1
    INVALID = -1

    if value >= 0: # Checks if the value is >= 0
        if from_units != 'm': # Starting units are converted into meters to begin
            if from_units == 'cm':
                value = value / CENTIMETER
                from_units = 'm'
            elif from_units == 'km':
                value = value / KILOMETER
                from_units = 'm'
            elif from_units == 'in':
                value = value / INCH
                from_units = 'm'
            elif from_units == 'ft':
                value = value / FOOT
                from_units = 'm'
            elif from_units == 'yd':
                value = value / YARD
                from_units = 'm'
            elif from_units == 'mi':
                value = value / MILE
                from_units = 'm'
            else:
                return INVALID # If the starting units are invalid, -1 is printed

        if to_units == 'cm': # Starting units are converted from meters into the target units
            dist = value * CENTIMETER
        elif to_units == 'km':
            dist = value * KILOMETER
        elif to_units == 'in':
            dist = value * INCH
        elif to_units == 'ft':
            dist = value * FOOT
        elif to_units == 'yd':
            dist = value * YARD
        elif to_units == 'mi':
            dist = value * MILE
        elif to_units == 'm':
            dist = value
        else:
            return INVALID # If the target units are invalid, -1 is printed

        return dist # The converted distance is returned
    else:
        print('Error! Cannot have negative distance.') # If the value entered is not >= 0, an error message is printed

def volume(value, from_units, to_units):
    '''
    Function: volume -- convert volumes
    Parameters: value -- the volume to be converted
                from_units -- the abbreviation of the starting volume
                to_units -- the abbreviation of the target volume
    Returns converted volume, or
            -1 if the from_units or to_units are invalid
    '''
    LITER = 1 # Conversion numbers based on 1 liter are input as constants for conversions
    CUP = 4.2267528377
    QUART = 1.0566882094
    GALLON = 0.2641720524
    INVALID = -1

    if value >= 0: # Checks if the value is >= 0
        if from_units != 'l': # Starting units are converted into liters to begin
            if from_units == 'cup':
                value = value / CUP
                from_units = 'l'
            elif from_units == 'qt':
                value = value / QUART
                from_units = 'l'
            elif from_units == 'gal':
                value = value / GALLON
                from_units = 'l'
            else:
                return INVALID # If the starting units are invalid, -1 is printed

        if to_units == 'cup': # Starting units are converted from liters into the target units
            vol = value * CUP
        elif to_units == 'qt':
            vol = value * QUART
        elif to_units == 'gal':
            vol = value * GALLON
        elif to_units == 'l':
            vol = value
        else:
            return INVALID # If the target units are invalid, -1 is printed
    
        return vol # The converted volume is returned
    else:
        print('Error! Cannot have negative volume.') # If the value entered is not >= 0, an error message is printed

def weight(value, from_units, to_units):
    '''
    Function: weight -- convert weights
    Parameters: value -- the weight to be converted
                from_units -- the abbreviation of the starting weight
                to_units -- the abbreviation of the target weight
    Returns converted weight, or
            -1 if the from_units or to_units are invalid
    '''
    POUND = 1 # Conversion numbers based on 1 pound are input as constants for conversions
    OUNCE = 16
    TON = 0.0005
    GRAM = 453.59237
    KILOGRAM = 0.45359237
    STONE = 0.0714285714
    INVALID = -1

    if value >= 0: # Checks if the value is >= 0
        if from_units != 'lb': # Starting units are converted into pounds to begin
            if from_units == 'oz':
                value = value / OUNCE
                from_units = 'lb'
            elif from_units == 'ton':
                value = value / TON
                from_units = 'lb'
            elif from_units == 'gr':
                value = value / GRAM
                from_units = 'lb'
            elif from_units == 'kg':
                value = value / KILOGRAM
                from_units = 'lb'
            elif from_units == 'st':
                value = value / STONE
                from_units = 'lb'
            else:
                return INVALID # If the starting units are invalid, -1 is printed

        if to_units == 'oz': # Starting units are converted from pounds into the target units
            wt = value * OUNCE
        elif to_units == 'ton':
            wt = value * TON
        elif to_units == 'gr':
            wt = value * GRAM
        elif to_units == 'kg':
            wt = value * KILOGRAM
        elif to_units == 'st':
            wt = value * STONE
        elif to_units == 'lb':
            wt = value
        else:
            return INVALID # If the target units are invalid, -1 is printed
    
        return wt # The converted weight is returned
    else:
        print('Error! Cannot have negative weight.') # If the value entered is not >= 0, an error message is printed

def temperature(value, from_units, to_units):
    '''
    Function: temperature -- convert temperature
    Parameters: value -- the temperature to be converted
                from_units -- the abbreviation of the starting temperature
                to_units -- the abbreviation of the target temperature
    Returns converted temperature, or
            -1 if the from_units or to_units are invalid
    '''
    INVALID = -1
    ABSOLUTE_C = -273
    ABSOLUTE_F = -459.40000000000003

    if from_units == 'C': # If starting units are Celsius, the value is converted into Fahrenheit
        if value >= ABSOLUTE_C: # Checks if the value is >= Absolute Zero
            temp = 9/5 * value + 32
            if to_units != 'F':
                return INVALID # If the starting units are invalid, -1 is printed
            return temp # The converted temperature is returned
        else:
            print('Error! Cannot have temperature below Absolute Zero.') # If the value entered is not >= -273, an error message is printed
    elif from_units == 'F': # If starting units are Fahrenheit, the value is converted into Celsius
        if value >= ABSOLUTE_F: # Checks if the value is >= Absolute Zero
            temp = 5/9 * (value - 32)
            if to_units != 'C':
                return INVALID # If the starting units are invalid, -1 is printed
            return temp # The converted temperature is returned
        else:
            print('Error! Cannot have temperature below Absolute Zero.') # If the value entered is not >= -273, an error message is printed        
    else:
        return INVALID # If the target units are invalid, -1 is printed

if __name__ == '__main__':
    main()