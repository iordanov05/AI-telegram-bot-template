import logging
import sys

def setup_logger() -> logging.Logger:
    logger = logging.getLogger("ai-telegram-bot")
    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(handler)

    logger.propagate = False
    return logger

logger = setup_logger()
