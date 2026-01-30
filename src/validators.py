def validate_symbol(symbol: str):
    """
    Validates if the trading symbol is a valid USDT pair.
    Example: BTCUSDT, ETHUSDT
    """
    if not isinstance(symbol, str):
        raise ValueError("Symbol must be a string")

    symbol = symbol.upper()

    if not symbol.endswith("USDT"):
        raise ValueError("Invalid symbol. Only USDT pairs are allowed (e.g., BTCUSDT)")

    return symbol


def validate_quantity(qty):
    """
    Validates that quantity is a positive float.
    """
    try:
        qty = float(qty)
    except ValueError:
        raise ValueError("Quantity must be a number")

    if qty <= 0:
        raise ValueError("Quantity must be greater than 0")

    return qty


def validate_price(price):
    """
    Validates that price is a positive float.
    """
    try:
        price = float(price)
    except ValueError:
        raise ValueError("Price must be a number")

    if price <= 0:
        raise ValueError("Price must be greater than 0")

    return price
