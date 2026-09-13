def calculate_discount(price, discount):
    """Calculates the final price of a product after applying a given discount percentage."""
    discounted_price = price*(discount/100)
    return (price - discounted_price)

# "If it looks like a duck and quacks like a duck, it's a duck"