import logging
import datetime
import functools
import time
import socket
import uuid
import json

from uds_socket import SimpleDGRAMSocket


logger = logging.getLogger("metrics.agent")
handler = logging.StreamHandler()
formatter = logging.Formatter("%(message)s")
handler.setFormatter(formatter)
if not logger.handlers:
    logger.addHandler(handler)
logger.setLevel("DEBUG")
logger.info("{}".format({"event": "metrics_emitter_start"}))


def timed(name):
    """
    Timer decorator

    :param name:
    :return:
    """
    metrics = dict(
        environment='development',
        guid=str(uuid.uuid4()),
        host=socket.gethostname().lower(),
        name=name
    )

    def wrapper(func):
        @functools.wraps(func)
        def inner(*f_args, **f_kwargs):
            response = error = None
            start = time.time()
            logger.info(
                "{}".format(
                    dict(
                        event="{0}_start".format(name),
                        arguments=f_args,
                        start_time=datetime.datetime.now().isoformat()
                    )
                )
            )
            try:
                response = func(*f_args, **f_kwargs)
            except Exception as e:
                error = e
                metrics['error'] = dict(
                    count=1
                )
            finally:
                duration = (time.time() - start) * 1000
                logger.info(
                    "{}".format(
                        dict(
                            event="{0}_end".format(name),
                            arguments=f_args,
                            error=error,
                            end_time=datetime.datetime.now().isoformat(),
                            duration="{0}ms".format(duration)
                        )
                    )
                )
                metrics['timer'] = dict(
                    count=1,
                    duration=duration
                )
                emit(metrics)
                if error:
                    raise error
            return response
        return inner
    return wrapper


def emit(metrics):
    write_data = json.dumps(metrics)
    write_data = write_data.encode()
    SimpleDGRAMSocket().send(write_data)
