#Given 2 int values, return True if one is negative and one is positive. Except if the parameter "negative" is True, then return True only if both are negative.
def pos_neg(a, b, negative):
    if negative:
        return (a < 0) and (b < 0)  
    return (a < 0) != (b < 0)  

#Given an array of ints length 3, figure out which is larger, the first or last element in the array, and set all the other elements to be that value. Return the changed array.
def max_end3(nums):
    big = max(nums[0]. nums[-1])
    nums[0] = big 
    nums[1] = big
    nums[2] = big
    return nums

#bricks problem (big = 5, small = 1)
def make_bricks(small, big, goal):
    big_used = min(big, goal // 5)    #you are trying to use AM big AP
    remainder = goal - big_used * 5
    return remainder <= small
