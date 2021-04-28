import logging
import time


def sleep(seconds):
    logging.debug("sleeping for {}".format(seconds))
    time.sleep(seconds)
