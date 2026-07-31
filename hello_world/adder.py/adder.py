import argparse
import time

parser = argparse.ArgumentParser()

parser.add_argument('greeting', help = 'The greeting message displayed')
parser.add_argument('-n', '--numbers', type = float, nargs = '*', help = 'numbers we are adding')
parser.add_argument('-v', '--verbosity', type = int, choices = [0, 1, 2], help = 'amount of information we are giving out')
parser.add_argument('-f', '--file', type = str)
parser.add_argument('--time', action = 'store_true', help = 'enables timer mode')  #this is a boolean flag. No input = False; input = True

args = parser.parse_args()


output = ''
if args.time:
    start = time.perf_counter()
if args.numbers is None or args.verbosity is None:
    output += args.greeting + '\n'
else:
    if args.verbosity >= 0:
        output += args.greeting + '\n'
    if args.verbosity >=1:
        output += 'Sum = ' + str(sum(args.numbers)) + '\n'
    if args.verbosity == 2:
        import math
        output += 'Numbers Multipled = ' + str(math.prod(args.numbers)) + '\n'
if args.time:
    end = time.perf_counter()
    output += 'time taken = ' + str(end - start) + ' (seconds)'


if args.file is not None:
    with open(args.file, 'w', encoding = 'utf-8') as f:
        f.write(output)
else:
    print(output)

    
#Important note regarding args.file: there are 3 different operations you can do:
# 1. write 'w' or append 'a': 
    # with open(args.file, 'w' or 'a') as nickname:
    #   nickname.write(output)         the .write() stays the same
# 2. read 'r':
    # with open(args.file, 'r') as nickname:
    #   contents = nickname.read()     the () stays empty


    



