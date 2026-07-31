for x in range(1):
    for y in range(3):
        print(f"({x}, {y})")
#range function is a complex type that is iterable

for a in "Python": #a string is also iterable
    print(a)

for b in [1, 2, 3, 4]: #a list (of numbers or strings)
    print(b)


# for item in ingredient_list: 
#     print(item)
#here ingredient list is a custom object. We can use it in a for_loop, and for each iteration we can get one item and print it