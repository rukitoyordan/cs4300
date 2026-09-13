from sympy import isprime

def check_number_status(number):
    if(number) > 0:
        return "this number is positive."
    elif(number) < 0:
        return "this number is negative."
    else:
        return "this number is zero."

# https://www.geeksforgeeks.org/python/python-program-to-check-whether-a-number-is-prime-or-not/
def first_ten_prime_numbers():
    prime_numbers = []

    for number in range(2,2000):
        if len(prime_numbers) == 10:
            break
        if isprime(number):
            prime_numbers.append(number)
            print(number)
    return prime_numbers

# Sum is 5050
def sum_all_one_to_hundred():
    sum = 0
    count = 0

    while count <= 100:
        sum += count
        count += 1
    return sum