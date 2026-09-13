# Integers
def integer_mult(int1, int2):
    """Multiplies two integers and returns the resulting multiplication."""
    return int1 * int2

# Floating-Point Numbers
def float_division(float1, float2):
    """Divides two floats and returns the resulting division."""
    return float1/float2

# String
def string_invert(str):
    """Inverts a provided string using a list slicing."""
    string_reversed = str[::-1]
    return string_reversed

# Boolean
def is_capitalized(str):
     """Verifies if a string is completely capitalized or not. Returns True if fully capitalized, otherwise False."""
    return str.isupper()
