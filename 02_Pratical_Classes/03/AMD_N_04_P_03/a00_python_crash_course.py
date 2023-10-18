# to use accented characters in the code
# -*- coding: cp1252 -*-
# ===============================
# author: Paulo Trigo Silva (PTS)
# ____________________
# Python Crash-Course
# ===============================

# Function for Strings
def explore_strings():
    # Strings
    # notice how you can access characters in the string using array syntax
    data = 'hello world'
    print(data[0])
    print(len(data))
    print(data)

# Function for Numbers
def explore_numbers():
    # Numbers
    value = 123.1
    print(value)
    value = 10
    print(value)

# Function for Boolean
def explore_boolean():
    # Boolean
    a = True
    b = False
    print(a, b)

# Function for Multiple Assignment
def explore_multiple_assignment():
    # Multiple Assignment
    # This can also be very handy for unpacking data in simple data structures
    a, b, c = 1, 2, 3
    print(a, b, c)

# Function for No value
def explore_no_value():
    # No value
    a = None
    print(a)

# Function for Flow Control
def explore_flow_control():
    # Flow Control
    # There are three main types of flow control that you need to learn:
    # If-Then-Else conditions, For-Loops and While-Loops

    # If-Then-Else
    value = 60
    if value < 60:
        print('That is safe')
    elif value < 120:
        print('That is fast')
    else:
        print('That is too fast')

    # For-Loop
    for i in range(10):
        print(i)

    # While-Loop
    i = 0
    while i < 10:
        print(i)
        i += 1

# Function for Data Structures
def explore_data_structures():
    # Data Structures
    # There are three data structures in Python that you will find the most used and useful.
    # They are tuples, lists, and dictionaries

    # Tuple (cannot change - immutable)
    # read-only collections of items
    a = (1, 2, 3)
    print(a)

    # Lists
    # use the square bracket notation and can be indexed using array notation
    # Notice that we are using some simple printf-like
    # functionality to combine strings and variables when printing
    mylist = [1, 2, 3]
    print("Zeroth Value: %d" % mylist[0])
    mylist.append(4)
    print("List Length: %d" % len(mylist))
    for value in mylist:
        print(value)

    # Dictionaries
    # mappings of names to values, like key-value pairs
    # Note the use of the curly bracket, and
    # colon notations when defining the dictionary
    mydict = {'a': 1, 'b': 2, 'c': 3}
    print("A value: %d" % mydict['a'])
    mydict['a'] = 11
    print("A value: %d" % mydict['a'])
    print("Keys: %s" % mydict.keys())
    print("Values: %s" % mydict.values())
    for key in mydict.keys():
        print(mydict[key])

# Function for Functions
def explore_functions():
    # Functions
    # The biggest gotcha with Python is the whitespace
    # Ensure that you have an empty new line after indented code

    # Sum function
    def mysum(x, y):
        return x + y

    # Test sum function
    x = mysum(1000, 3333)
    print(x)

# Main function
def main():
    explore_strings()
    explore_numbers()
    explore_boolean()
    explore_multiple_assignment()
    explore_no_value()
    explore_flow_control()
    explore_data_structures()
    explore_functions()

    # Call other functions for each section

if __name__ == "__main__":
    main()