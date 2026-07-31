# 1: a function performs a task:
def greet(first_name, last_name): #first ane last names are parameters 
    print(f"Hi {first_name} {last_name}")
    print("Welcome")


greet("Josh", "Li") #this is an argument(s) for the given parameter
 

# 2: a function returns a value
def get_greeting(name):
    return f"Hi {name}"


message = get_greeting("Jerry")
print(message)