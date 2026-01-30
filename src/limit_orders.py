from src.client import BinanceClient
from src.validators import validate_symbol, validate_quantity, validate_price
from src.logging_config import logger
from binance.exceptions import BinanceAPIException


def validate_side(side):
    """Ensure BUY or SELL is valid."""
    valid_sides = ["BUY", "SELL"]
    if side.upper() not in valid_sides:
        raise ValueError("Side must be either BUY or SELL")
    return side.upper()


def place_limit_order(symbol, side, quantity, price):
    """Place a LIMIT order on Binance Futures."""

    # Use cleaned values
    symbol = validate_symbol(symbol)
    quantity = validate_quantity(quantity)
    price = validate_price(price)
    side = validate_side(side)

    logger.info(f"Placing LIMIT {side} → {symbol} | qty={quantity}, price={price}")

    try:
        client = BinanceClient().get_client()

        response = client.futures_create_order(
            symbol=symbol,
            side=side,
            type="LIMIT",
            quantity=quantity,
            price=price,
            timeInForce="GTC"
        )

        logger.info(f"Limit Order Success: {response}")
        print("Limit order placed successfully!")
        return response

    except BinanceAPIException as e:
        logger.error(f"Binance API Error: {e.message}")
        print("Binance API Error:", e.message)

    except Exception as e:
        logger.error(f"Error placing limit order: {e}")
        print("Error:", str(e))


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 5:
        print("Usage: python -m src.limit_orders <symbol> <BUY/SELL> <quantity> <price>")
        exit()

    _, symbol, side, qty, price = sys.argv
    place_limit_order(symbol, side, qty, price)
