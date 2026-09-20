def calculate_discount(price, discount):
    """Calculates the final price of a product after applying a given discount percentage."""
    try:
        if price < 0 or discount < 0 or discount > 100:
            raise ValueError("Please provide valid pricing and discount percentage amounts.")
    discounted_price = price*(discount/100)
    return (price - discounted_price)
    except TypeError as numeric_error:
        raise TypeError("Please provide a numeric pricing and discount percentage, rather than a string.") from numeric_error


# "If it looks like a duck and quacks like a duck, it's a duck"