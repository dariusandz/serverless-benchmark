import logging
import sys

from logging import INFO


def init_logging(level=INFO):
    root = logging.getLogger()
    root.setLevel(level)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)

    formatter = logging.Formatter(
        "[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    root.addHandler(handler)


def log(message, log_level=INFO):
    logging.log(log_level, message)
