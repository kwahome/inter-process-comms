import os

from sender import send_metrics_to_remote_storage
from uds_socket import UDS


import logging
import asyncio

logger = logging.getLogger("metrics.collector")
handler = logging.StreamHandler()
formatter = logging.Formatter("%(message)s\n\n")
handler.setFormatter(formatter)
if not logger.handlers:
    logger.addHandler(handler)
logger.setLevel("DEBUG")

logger.info("{}".format({"event": "metrics_collector_start"}))


async def collect_metrics():
    try:
        logger.info("{}".format({"event": "metrics_collector_read"}))
        while True:
            data = UDS().receive()
            if len(data) == 0:
                # End of the file
                await asyncio.sleep(1)
                continue
            logger.info(
                "{}".format(
                    {
                        "event": "metrics_collector_print_data", "data": data
                    }
                )
            )
            await send_metrics_to_remote_storage(data=data)
    except Exception as e:
        logger.debug("{}".format({"event": "metrics_collector_error", "error": str(e)}))
        raise e


loop = asyncio.get_event_loop()
loop.run_until_complete(collect_metrics())
loop.close()
logger.info("{}".format({"event": "metrics_collector_end"}))
