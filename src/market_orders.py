from src.logging_config import logger
from src.client import BinanceClient
from src.validators import validate_symbol, validate_quantity
from binance.exceptions import BinanceAPIException


def validate_side(side):
    """Validate BUY/SELL input"""
    valid_sides = ["BUY", "SELL"]

    if side.upper() not in valid_sides:
        raise ValueError("Side must be either BUY or SELL")

    return side.upper()


def place_market_order(symbol, side, quantity):
    """Place a MARKET order on Binance Futures"""

    # Validate inputs
    symbol = validate_symbol(symbol)
    quantity = validate_quantity(quantity)
    side = validate_side(side)

    logger.info(f"MARKET {side} → {symbol} | qty={quantity}")

    try:
        client = BinanceClient().get_client()

        response = client.futures_create_order(
            symbol=symbol,
            side=side,
            type="MARKET",
            quantity=quantity
        )

        logger.info(f"Order Success: {response}")
        print("Order placed successfully!")
        return response

    except BinanceAPIException as e:
        logger.error(f"Binance API Error: {e.message}")
        print("Binance API Error:", e.message)

    except Exception as e:
        logger.error(f"Unknown Error: {str(e)}")
        print("Error:", str(e))
