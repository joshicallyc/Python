x = input("x: ") #input() always gives a string, or text. So here 1 is the text 1
y = int(x) + 1 #this converts the text 1 to the number 1, then adds 1
print(f"x: {x}, y: {y}") #an f before "" makes this an f-string, which allows you to put variables inside the string. The {} is where the variable goes. So this prints x: 1, y: 2
# an f-string is useful when you want to give a value to some text. 
price = 10
tax = 2
print(f"the total is ${price + tax}") #example


#these are all built in functions
# int(x)
# float(x)
# bool(x), though falsy values are: "", 0, None
# str(x)

print(bool("False")) #this is True, because the string is not empty. The string "False" is not the same as the boolean False.