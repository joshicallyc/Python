course = "Python Programming"
print(len(course)) #len = length of the string. It's a function and takes in an input
print(course[0]) #use [] to access a specific element or character in a string. 
print(course[-1]) #locates last character
print(course[0:3]) #does not include "3"

course = "Python \"Programming" #\ can be used to escape the character after it. (if you do \\ it will show one \)
print(course)
new_line = "Python \nProgramming" # \n creates a new line
print(new_line)

first = "Josh"
last = "Li"
full = f"{first} {last}" # you can input any expression in {}. eg you can input len(first) here and it will give you 4 (Josh has 4 letters)
print(full)
#f"" is an f-string, which allows u to mix text with variable values. You would insert the valuable in {}

name = "Josh Li"
print(name.upper())
print(name.lower())
print(name.title()) #capitalizes the first letter of each word in the string    
name = "  epicJosh Li"
print(name.strip()) #removes whitespace from the beginning and end of the string
print(name.lstrip()) #removes whitespace from the left side of the string
print(name.rstrip()) #removes whitespace from the right side of the string
print(name.find("osh")) #finds the index of the first occurrence of the substring. If not found, returns -1
print(name.replace("o", "sigma")) #replaces the first argument with the second argument
print("epic" in name) #checks if the substring is in the string, returns True or False
print("gyat" not in name) #checks if the substring is not in the string, returns True or False

#missing character exercise:
def missing_char(text, n):
    return text[:n] + text[(n+1):] #[n:] means slicing from n to the end

print(missing_char("epicjoshy", 3))


x = "hello"
print(x[len(x)-1])