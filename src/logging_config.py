import logging

LOG_FILE = "bot.log"

def setup_logger():
    logger = logging.getLogger("binance_bot")
    logger.setLevel(logging.INFO)

    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        "%(asctime)s - [%(levelname)s] - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    file = logging.FileHandler(LOG_FILE)
    file.setFormatter(formatter)

    console = logging.StreamHandler()
    console.setFormatter(formatter)

    logger.addHandler(file)
    logger.addHandler(console)

    return logger

logger = setup_logger()
