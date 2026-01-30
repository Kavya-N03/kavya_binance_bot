# src/advanced/grid_strategy.py

from src.client import BinanceClient
from src.validators import validate_symbol, validate_quantity, validate_price
from src.logging_config import logger
from binance.exceptions import BinanceAPIException


def validate_side(side):
    side = side.upper()
    if side not in ["BUY", "SELL"]:
        raise ValueError("Side must be BUY or SELL")
    return side


def grid_strategy(symbol, side, total_quantity, lower_price, upper_price, grids):
    """
    Simple Grid Trading Strategy for Binance Futures.

    Places multiple LIMIT orders between a price range.
    """

    # Validations and conversions
    symbol = validate_symbol(symbol)
    total_quantity = validate_quantity(total_quantity)
    lower_price = validate_price(lower_price)
    upper_price = validate_price(upper_price)
    side = validate_side(side)

    if lower_price >= upper_price:
        raise ValueError("Lower price must be LESS than upper price")

    if grids < 2:
        raise ValueError("Grid levels must be 2 or more")

    grids = int(grids)
    qty_per_grid = total_quantity / grids
    validate_quantity(qty_per_grid)

    price_step = (upper_price - lower_price) / grids

    logger.info(
        f"GRID START → {symbol} | Side={side}, Qty={total_quantity}, Grids={grids}, Range={lower_price}-{upper_price}"
    )

    print("=" * 50)
    print("GRID TRADING STRATEGY")
    print(f"Symbol         : {symbol}")
    print(f"Side           : {side}")
    print(f"Total Quantity : {total_quantity}")
    print(f"Grids          : {grids}")
    print(f"Qty per grid   : {qty_per_grid}")
    print(f"Price range    : {lower_price} → {upper_price}")
    print("=" * 50)

    client = BinanceClient().get_client()
    responses = []

    # Create LIMIT orders across the grid
    for i in range(grids):
        grid_price = lower_price + (i * price_step)
        rounded_price = round(grid_price, 2)  # May vary depending on symbol tick size

        try:
            logger.info(f"Grid Order {i+1}/{grids} → Price={rounded_price}, Qty={qty_per_grid}")

            response = client.futures_create_order(
                symbol=symbol,
                side=side,
                type="LIMIT",
                quantity=qty_per_grid,
                price=rounded_price,
                timeInForce="GTC"
            )

            responses.append(response)
            print(f"Placed grid order {i+1}/{grids} at price {rounded_price}")

        except BinanceAPIException as e:
            logger.error(f"Binance API Error (GRID): {e.message}")
            print("Binance API Error:", e.message)

        except Exception as e:
            logger.error(f"Unknown Error (GRID): {str(e)}")
            print("Error:", str(e))

    print("Grid Strategy Orders Created!")
    logger.info("GRID STRATEGY COMPLETED")

    return responses


if __name__ == "__main__":
    """
    Example:
    python -m src.advanced.grid_strategy BTCUSDT BUY 0.1 40000 45000 5
    """
    import sys

    if len(sys.argv) != 7:
        print("Usage: python -m src.advanced.grid_strategy <symbol> <BUY/SELL> <total_qty> <lower_price> <upper_price> <grids>")
        exit()

    _, symbol, side, qty, low, high, grids = sys.argv

    grid_strategy(
        symbol,
        side,
        float(qty),
        float(low),
        float(high),
        int(grids)
    )
