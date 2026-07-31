def multiply(*numbers): #* means: multiply(2, 3, 4, 5)
    result = 1
    for number in numbers:
        result *= number
    return result 

print(multiply(2, 3, 4, 5))

#(2, 3, 4, 5) is a tuple, a collection data type used to store multiple items in a single variable. Unlike lists, tuples cannot be changed, but both are iterable (so we can use them for loops).