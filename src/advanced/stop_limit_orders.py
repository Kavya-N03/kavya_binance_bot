# src/stop_limit_orders.py

from src.client import BinanceClient
from src.validators import validate_symbol, validate_quantity, validate_price
from src.logging_config import logger
from binance.exceptions import BinanceAPIException


def validate_side(side):
    valid_sides = ["BUY", "SELL"]
    side = side.upper()
    if side not in valid_sides:
        raise ValueError("Side must be BUY or SELL")
    return side


def place_stop_limit_order(symbol, side, quantity, stop_price, limit_price):
    """
    STOP-LIMIT Order (Futures)
    stop_price → trigger price
    limit_price → order placed after trigger
    """

    # Clean validated values
    symbol = validate_symbol(symbol)
    quantity = validate_quantity(quantity)
    stop_price = validate_price(stop_price)
    limit_price = validate_price(limit_price)
    side = validate_side(side)

    logger.info(
        f"STOP-LIMIT {side} → {symbol} | qty={quantity}, stop={stop_price}, limit={limit_price}"
    )

    try:
        client = BinanceClient().get_client()

        response = client.futures_create_order(
            symbol=symbol,
            side=side,
            type="STOP",          # STOP + price → STOP-LIMIT order
            stopPrice=stop_price,
            price=limit_price,
            quantity=quantity,
            timeInForce="GTC"
        )

        logger.info(f"Stop-Limit Order Success: {response}")
        print("Stop-Limit order placed successfully!")
        return response

    except BinanceAPIException as e:
        logger.error(f"Binance API Error (STOP-LIMIT): {e.message}")
        print("Binance API Error:", e.message)

    except Exception as e:
        logger.error(f"Unknown Error (STOP-LIMIT): {e}")
        print("Error:", str(e))


if __name__ == "__main__":
    """
    Run using:
    python -m src.stop_limit_orders BTCUSDT BUY 0.01 42000 42500
    """
    import sys

    if len(sys.argv) != 6:
        print(
            "Usage: python -m src.stop_limit_orders <symbol> <BUY/SELL> <qty> <stop_price> <limit_price>"
        )
        exit()

    _, symbol, side, qty, sp, lp = sys.argv
    place_stop_limit_order(symbol, side, qty, sp, lp)
