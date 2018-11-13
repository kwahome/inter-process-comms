import os
import errno


MODE = 0o777


class NamedPipe:
    """

    """
    def __init__(self, _dir="/tmp/namedPipes", file_name="simpleNamedPipe"):
        self._dir = os.getenv("METRICS_FIFO_DIR", _dir)
        self._file_name = os.getenv("METRICS_FIFO_NAME", file_name)
        self._path = os.path.join(self._dir, self._file_name)

    @property
    def fifo_path(self):
        return self._path

    def _make_dir(self):
        try:
            os.mkdir(self._dir, MODE)
        except OSError as e:
            if e.errno == 17:  # dir exists
                pass
            else:
                raise e
        return

    def _make_file(self):
        try:
            os.mkfifo(self.fifo_path, MODE)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise e
        return

    def make_fifo(self):
        self._make_dir()
        self._make_file()
        return self.fifo_path
