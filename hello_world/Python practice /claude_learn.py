
#functions. we did this before
def greet(name, greeting = "hello"):
    return f"{greeting} {name}!"

print(greet("Josh"))
print(greet("Josh", "你好!"))


#data structures:
#1. List, an ordered, changeable collection. 
fruits = ["apples", "strawberries", "pineapple"]
fruits.append("oranges") #add to the end
fruits[0] = "banana" #change an item
fruits.remove("pineapple")
print(fruits[1])

a = [1, 2]
b = [2, 3]
print(a + b)
print(a * 3)

#2. Tuple, an order, NOT changeable collection. More memory efficient than lists. Use when RGB colors, coordinates. 
coordinates = (0.42, 3.41) 
#+ and * also works the same for tuples

#3.  Dictionaries (dict). Access through labeling rather than position
student = {
    "name": "Josh Li",
    "age": 18,
    "major": "Bioengineering"
}
print(student["name"])
student["age"] = 19   #update a value
student["hobby"] = "baking"   #add a new key/label
print(student["hobby"])

#4. Sets, unordered collection of unique items (duplicates automatically removed)
tags = {"cookies", "cheesecake", "dairy"}
print(tags)

a = {1, 2, 3}
b = {2, 4, 5}
print(a & b)  #intersection. prints the common one
print(a | b)  #union
print(a - b)  #different ones in a from b 
print(b - a)  #different ones in b from a   
