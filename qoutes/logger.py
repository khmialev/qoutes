import logging
import sys
from logging import Logger



def setup_logger(log_file: str) -> Logger:
    logger = logging.getLogger("quotes_scraper")
    logger.setLevel(logging.INFO)

    logger.propagate = False

    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        fmt="[%(asctime)s] %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Лог в файл
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Лог в консоль (stdout, а не stderr)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger


