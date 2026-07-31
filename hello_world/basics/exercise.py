# write a program that display even numbers between 1-10, and print the message "we have 4 even numbers"
count = 0
for number in range(1, 10):
    if number % 2 == 0: #remember "=" assigns a value to variable, while "==" compares two value if they are equal
        count += 1
        print(number)

print(f"we have {count} even numbers")

