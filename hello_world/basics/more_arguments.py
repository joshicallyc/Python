# def increment(number, by):
#     return number + by


# print(increment(2, by=1))

# you can also make the "by" argument optional by:
def increment(steak_temp, by=15): #here we give by a default value. Remember optional parameters must come AFTER required parameters
    return steak_temp + by


print(increment(115, 20)) #here the argument "20" overides the optional default value "15"

