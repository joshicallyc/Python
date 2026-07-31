v_shape = False
for number in range(1, 4, 1): #first two arguments give range, third argument gives step
    print("egg", "*", number)
    if v_shape:
        print("good to pipe")
        break
else:
    print("keep slowly adding eggs")