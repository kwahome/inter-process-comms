#!/usr/bin/python
import logging
import socket
import errno


logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(message)s")
handler.setFormatter(formatter)
if not logger.handlers:
    logger.addHandler(handler)
logger.setLevel("DEBUG")
logger.info("{}".format({"event": "metrics_emitter_start"}))


class UDS:
    """

    """

    def __init__(self, name="simple-socket.sock", _type=socket.SOCK_DGRAM):
        self._name = name
        self._socket = socket.socket(family=socket.AF_UNIX, type=_type)
        #  \0 for Linux Abstract Socket Namespace
        self._sock_addr = "/tmp/uds-socket-%s" % name
        self.socket_bind()

    @property
    def socket_addr(self):
        return self._sock_addr

    def socket_bind(self):
        try:
            self._socket.bind(self.socket_addr)
        except OSError as e:
            if e.errno == errno.ENOSR:
                self._socket.connect(self.socket_addr)
            else:
                raise e

    def receive(self):
        while True:
            data, _ = self._socket.recvfrom(1024)
            logger.info(
                "{}".format(
                    {
                        "event": "UDS_socket_receive",
                        "data": data
                    }
                )
            )

    def send(self, data):
        logger.info(
            "{}".format(
                {
                    "event": "UDS_socket_send",
                    "data": data
                }
            )
        )
        self._socket.sendto(data, self.socket_addr)
