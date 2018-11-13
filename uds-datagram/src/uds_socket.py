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
SOCK_NAME = os.getenv("SOCKET_NAME", "metrics")
SERVER_ADDR = "/tmp/uds/%s.sock" % SOCK_NAME


class DGRAMSocket:
    def __init__(self):
        self._family = socket.AF_UNIX
        self._type = socket.SOCK_DGRAM
        self._sock = socket.socket(family=self._family, type=self._type)

    @property
    def socket(self):
        return self._sock


class Client:
    """
    Datagram socket client
    """
    def __init__(self):
        self.socket = DGRAMSocket().socket

    def send(self, data, recp=SERVER_ADDR):
        logger.info(
            "{}".format(
                {
                    "event": "UDS_socket_send",
                    "data": data,
                    "recipient": recp
                }
            )
        )
        self.socket.sendto(data, recp)


class Server:
    """
    Datagram socket server
    """

    def __init__(self):
        self.socket = DGRAMSocket().socket
        self.bind()

    def bind(self):
        try:
            self.socket.bind(SERVER_ADDR)
        except OSError as e:
            if e.errno == errno.EADDRINUSE:
                os.unlink(SERVER_ADDR)
                self.bind()
            else:
                raise e

    def receive(self):
        while True:
            data, address = self.socket.recvfrom(BUFFER_SIZE)
            logger.info(
                "{}".format(
                    {
                        "event": "UDS_socket_receive",
                        "data": data,
                        "sender": address
                    }
                )
            )


class SimpleDGRAMSocket:
    """
    Alternative implementation with both client & server
    """
    def __init__(self, name="simple", server=False):
        self._name = name
        self._address = "/tmp/uds/%s.sock" % name
        self._family = socket.AF_UNIX
        self._type = socket.SOCK_DGRAM
        self._socket = socket.socket(family=self._family, type=self._type)
        if server:
            self.bind()
        # self._socket.setblocking(0)

    @property
    def address(self):
        return self._address

    @property
    def name(self):
        return self._name

    @property
    def socket(self):
        return self._socket

    def bind(self):
        try:
            self.socket.bind(self.address)
        except OSError as e:
            if e.errno == errno.EADDRINUSE:
                os.unlink(self.address)
                self.bind()
            else:
                raise e

    def receive(self):
        data, address = self.socket.recvfrom(BUFFER_SIZE)
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
                    "data": data,
                    "recipient": self.address
                }
            )
        )
        try:
            self.socket.sendto(data, self.address)
        except Exception as e:
            # no way to catch ConnectionRefusedError in Python 2 as it was
            # added in Python 3 builtins hence the workaround with errno
            if getattr(e, 'errno', None) == 111:
                logger.info(
                    "{}".format(
                        {
                            "event": "UDS_socket_connection_refused_error",
                            "error": e.__class__.__name__,
                            "message": str(e)
                        }
                    )
                )
            else:
                raise e
