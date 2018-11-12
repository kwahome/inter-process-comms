import random
import logging
import time
from agent import timed

logger = logging.getLogger("metrics.example")
handler = logging.StreamHandler()
formatter = logging.Formatter("%(message)s")
handler.setFormatter(formatter)
if not logger.handlers:
    logger.addHandler(handler)
logger.setLevel("DEBUG")


@timed('addition')
def add(a, b):
    return a + b


@timed('exception')
def exception():
    raise Exception("Houston! We have a problem!")


while True:
    result = add(random.randint(0, 9), random.randint(0, 9))
    logger.info(
        "{}".format(
            dict(
                event="while_loop",
                result=result
            )
        )
    )
    if result % 2 == 0:
        try:
            exception()
        except Exception as e:
            logger.info(
                "An exception of type `{0}` with message `{1}` occured".format(
                    e.__class__.__name__, str(e)
                ))
    time.sleep(1)
