# src/advanced/twap.py

import time
from src.client import BinanceClient
from src.validators import validate_symbol, validate_quantity
from src.logging_config import logger
from binance.exceptions import BinanceAPIException


def validate_side(side):
    side = side.upper()
    if side not in ["BUY", "SELL"]:
        raise ValueError("Side must be BUY or SELL")
    return side


def twap_order(symbol, side, total_quantity, parts, interval_seconds):
    """
    TWAP Strategy:
    Splits a large order into smaller market orders placed at fixed intervals.
    """

    # Validate main inputs
    symbol = validate_symbol(symbol)
    total_quantity = validate_quantity(total_quantity)
    side = validate_side(side)

    if parts <= 0:
        raise ValueError("Parts must be greater than 0")

    parts = int(parts)

    qty_per_order = total_quantity / parts
    validate_quantity(qty_per_order)

    logger.info(
        f"TWAP STARTED → {symbol} | Side={side}, Total={total_quantity}, Parts={parts}, Qty/Order={qty_per_order}, Interval={interval_seconds}"
    )

    print(f"Running TWAP strategy for {symbol}...")
    client = BinanceClient().get_client()

    order_responses = []

    for i in range(1, parts + 1):
        try:
            logger.info(f"Placing TWAP order {i}/{parts} | qty={qty_per_order}")

            response = client.futures_create_order(
                symbol=symbol,
                side=side,
                type="MARKET",
                quantity=qty_per_order
            )

            order_responses.append(response)
            print(f"Order {i}/{parts} executed.")
            logger.info(f"TWAP Order {i} Success: {response}")

        except BinanceAPIException as e:
            print("Binance API Error:", e.message)
            logger.error(f"Binance API Error (TWAP): {e.message}")

        except Exception as e:
            print("Error:", str(e))
            logger.error(f"Unknown Error (TWAP): {str(e)}")

        if i != parts:
            print(f"Waiting {interval_seconds} seconds...")
            time.sleep(interval_seconds)

    print("TWAP Strategy Completed!")
    logger.info("TWAP Completed Successfully")

    return order_responses


if __name__ == "__main__":
    """
    Example:
    python -m src.advanced.twap BTCUSDT BUY 0.05 5 10
    """
    import sys

    if len(sys.argv) != 6:
        print("Usage: python -m src.advanced.twap <symbol> <BUY/SELL> <total_quantity> <parts> <interval_seconds>")
        exit()

    _, symbol, side, total_qty, parts, interval = sys.argv

    twap_order(symbol, side, float(total_qty), int(parts), int(interval))
