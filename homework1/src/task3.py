from sympy import isprime

def check_number_status(number):
    """Checks if a given number is either positive, negative or zero. It returns a statement declaring what type the number is."""
    if(number) > 0:
        return "this number is positive."
    elif(number) < 0:
        return "this number is negative."
    else:
        return "this number is zero."

# https://www.geeksforgeeks.org/python/python-program-to-check-whether-a-number-is-prime-or-not/
def first_ten_prime_numbers():
    """Loops to print the first 10 prime numbers."""
    prime_numbers = []

    for number in range(2,2000):
        if len(prime_numbers) == 10:
            break
        if isprime(number):
            prime_numbers.append(number)
            print(number)
    return prime_numbers

def sum_all_one_to_hundred():
    '''Finds the sum of all numbers from 1 to 100. Sum is 5050'''
    sum = 0
    count = 0

    while count <= 100:
        sum += count
        count += 1
    return sum