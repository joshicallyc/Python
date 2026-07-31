crunchy_on_the_outside = False
chewy_on_the_inside = True
if crunchy_on_the_outside and chewy_on_the_inside:
    print("your cookie is fantastic!!")
else:
    print("not great, try again..")
# “and” operators: if both the conditions are True, the result will be True 

crunchy = False
chewy = False
if crunchy or chewy:
    print("the brownies are good!")
else:
    print("try again")
# "or" operators: if one or more of the conditions are True, result will be True.

medium_rare = True
good_crust = False
cold = True
if (medium_rare or good_crust) or not cold: #python evaluates this in sequence, meaning if the first "or" condition is already False, this inter expression will be False (short circuit)
    print("bon appetit")
else:
    print("cook another steak")