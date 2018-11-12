#!/usr/bin/python
import logging
import socket
import errno
import os


logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(message)s")
handler.setFormatter(formatter)
if not logger.handlers:
    logger.addHandler(handler)
logger.setLevel("DEBUG")
logger.info("{}".format({"event": "metrics_emitter_start"}))

BUFFER_SIZE = 4096


class UDS:
    """

    """

    def __init__(self, name="socket.sock", reader=False):
        self._name = name
        self._family = socket.AF_UNIX
        self._type = socket.SOCK_DGRAM
        self._reader = reader
        self._writer = not self._reader
        # \0: Linux Abstract Socket Namespace
        self.sock_addr = "\0/tmp/uds-%s" % self._name
        self.sock = socket.socket(family=self._family, type=self._type)
        self.initial()

        # self.sock.setblocking(0)

    def initial(self):
        self.bind()

    @property
    def address(self):
        return self.sock_addr

    def bind(self):
        try:
            self.sock.bind(self.address)
        except OSError as e:
            if e.errno == errno.ENOSR:
                os.unlink(self.address)
                self.bind()
            else:
                raise e

    def connect(self):
        self.sock.connect(self.address)

    def receive(self):
        while True:
            data, address = self.sock.recvfrom(BUFFER_SIZE)
            logger.info(
                "{}".format(
                    {
                        "event": "UDS_socket_receive",
                        "data": data,
                        "sender": address
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
        self.sock.sendto(data, self.address)
