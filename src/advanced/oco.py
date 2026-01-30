# src/advanced/oco.py

from src.client import BinanceClient
from src.validators import validate_symbol, validate_quantity, validate_price
from src.logging_config import logger
from binance.exceptions import BinanceAPIException
import time


def validate_side(side):
    valid = ["BUY", "SELL"]
    side = side.upper()
    if side not in valid:
        raise ValueError("Side must be BUY or SELL")
    return side


def place_oco_order(symbol, side, quantity, take_profit_price, stop_price, stop_limit_price):
    """
    Custom OCO implementation for Binance Futures.
    Futures API does NOT support native OCO orders,
    so we manually place:
    
    1. Take Profit Limit Order
    2. Stop Limit Order
    
    Then monitor and cancel the opposite order when one executes.
    """

    symbol = validate_symbol(symbol)
    quantity = validate_quantity(quantity)
    take_profit_price = validate_price(take_profit_price)
    stop_price = validate_price(stop_price)
    stop_limit_price = validate_price(stop_limit_price)
    side = validate_side(side)

    logger.info(
        f"OCO {side} → {symbol} | qty={quantity}, TP={take_profit_price}, Stop={stop_price}, SL={stop_limit_price}"
    )

    try:
        client = BinanceClient().get_client()

        # ================================
        # 1. Take Profit Limit Order
        # ================================
        tp_order = client.futures_create_order(
            symbol=symbol,
            side=side,
            type="TAKE_PROFIT",
            quantity=quantity,
            price=take_profit_price,
            stopPrice=take_profit_price,
            timeInForce="GTC"
        )

        tp_order_id = tp_order["orderId"]

        # ================================
        # 2. Stop-Limit Order
        # ================================
        sl_order = client.futures_create_order(
            symbol=symbol,
            side=side,
            type="STOP",
            quantity=quantity,
            stopPrice=stop_price,
            price=stop_limit_price,
            timeInForce="GTC"
        )

        sl_order_id = sl_order["orderId"]

        logger.info(f"OCO Orders Placed: TP={tp_order_id}, SL={sl_order_id}")
        print("OCO orders placed!")
        print(f"TP Order ID: {tp_order_id}")
        print(f"SL Order ID: {sl_order_id}")

        # ================================
        # 3. Monitor execution
        # ================================

        print("Monitoring orders (OCO behavior)...")

        while True:
            time.sleep(1)

            tp_status = client.futures_get_order(symbol=symbol, orderId=tp_order_id)
            sl_status = client.futures_get_order(symbol=symbol, orderId=sl_order_id)

            if tp_status["status"] == "FILLED":
                print("Take-profit executed. Cancelling Stop-Limit.")
                client.futures_cancel_order(symbol=symbol, orderId=sl_order_id)
                break

            if sl_status["status"] == "FILLED":
                print("Stop-Limit executed. Cancelling Take-Profit.")
                client.futures_cancel_order(symbol=symbol, orderId=tp_order_id)
                break

        logger.info("OCO logic completed successfully.")
        return {"tp_order": tp_status, "sl_order": sl_status}

    except BinanceAPIException as e:
        logger.error(f"Binance API Error (OCO): {e.message}")
        print("Binance API Error:", e.message)

    except Exception as e:
        logger.error(f"Unknown Error (OCO): {e}")
        print("Error:", str(e))


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 7:
        print("Usage: python -m src.advanced.oco <symbol> <BUY/SELL> <qty> <take_profit_price> <stop_price> <stop_limit_price>")
        exit()

    _, symbol, side, qty, tp, sp, sl = sys.argv
    place_oco_order(symbol, side, qty, tp, sp, sl)
