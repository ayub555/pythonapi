import logging
import os
from datetime import datetime

LOG_DIR = "logs"
LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


class DailyFileHandler(logging.Handler):
    """Writes to logs/hdfc_log_file_dd_mm_yyyy.log, switching files when the date changes."""

    def __init__(self, log_dir: str = LOG_DIR, encoding: str = "utf-8"):
        super().__init__()
        self.log_dir = log_dir
        self.encoding = encoding
        self._current_date = None
        self._stream = None
        os.makedirs(self.log_dir, exist_ok=True)

    def _filename_for_today(self):
        today = datetime.now().strftime("%d_%m_%Y")
        return os.path.join(self.log_dir, f"hdfc_log_file_{today}.log"), today

    def emit(self, record: logging.LogRecord) -> None:
        filename, today = self._filename_for_today()
        if today != self._current_date:
            if self._stream:
                self._stream.close()
            self._current_date = today
            self._stream = open(filename, "a", encoding=self.encoding)
        self._stream.write(self.format(record) + "\n")
        self._stream.flush()

    def close(self) -> None:
        if self._stream:
            self._stream.close()
        super().close()


def get_logger(name: str = "hdfc_api") -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter(fmt=LOG_FORMAT, datefmt=DATE_FORMAT)

        file_handler = DailyFileHandler()
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        logger.propagate = False

    return logger


logger = get_logger()
