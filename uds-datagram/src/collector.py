import logging
import asyncio

from sender import send_metrics_to_remote_storage
from uds_socket import SimpleDGRAMSocket


logger = logging.getLogger("metrics.collector")
handler = logging.StreamHandler()
formatter = logging.Formatter("%(message)s\n\n")
handler.setFormatter(formatter)
if not logger.handlers:
    logger.addHandler(handler)
logger.setLevel("DEBUG")

logger.info("{}".format({"event": "metrics_collector_start"}))


# def main():
#     from threading import Thread
#     thread = Thread(target=SimpleDGRAMSocket().receive())
#     thread.setDaemon(False)
#     thread.start()
#
#
# main()


async def collect_metrics():
    try:
        logger.info("{}".format({"event": "metrics_collector_read"}))
        while True:
            data = SimpleDGRAMSocket(server=True).receive()
            logger.info(
                "{}".format(
                    {
                        "event": "metrics_collector_print_data", "data": data
                    }
                )
            )
            await send_metrics_to_remote_storage(data=data)
    except Exception as e:
        logger.debug(
            "{}".format({"event": "metrics_collector_error", "error": str(e)})
        )
        raise e


loop = asyncio.get_event_loop()
loop.run_until_complete(collect_metrics())
loop.close()
logger.info("{}".format({"event": "metrics_collector_end"}))
