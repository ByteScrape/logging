import datetime
import logging
import re
import sys
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
from typing import Optional

from colorama import Fore, Style, init

# Initialize Colorama for Windows ANSI support
init(autoreset=True)

# Precompiled regex patterns
EMOJI_PATTERN = re.compile(
    r"["
    r"\U0001F600-\U0001F64F\U0001F300-\U0001F5FF"
    r"\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF"
    r"\u200d\u23cf\u23e9\u23ea-\u23ed\u23ef\u23f0-\u23f3"
    r"\u25A0-\u25FF\u2600-\u26FF\u2700-\u27BF\u2B00-\u2BFF"
    r"\U00010000-\U0010ffff]+",
    flags=re.UNICODE
)

SAFE_CHARS = re.compile(r'[^a-zA-Z0-9_\-\.\s]')


class EnhancedFormatter(logging.Formatter):
    COLOR_MAP = {
        logging.DEBUG: Fore.CYAN,
        logging.INFO: Fore.GREEN,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.WHITE + Style.BRIGHT + Fore.RED
    }

    def __init__(
        self,
        fmt: str,
        datefmt: Optional[str] = None,
        tty_only: bool = True
    ):
        super().__init__(fmt, datefmt)
        self.tty_only = tty_only
        self.use_colors = sys.stdout.isatty() or not tty_only

    def format(self, record):
        msg = super().format(record)
        msg = self._process_special_chars(msg)
        return self._apply_colors(msg, record.levelno)

    def _process_special_chars(self, msg):
        msg = msg.replace("\u2192", "-->")
        if any(ord(c) > 0x7f for c in msg):
            return EMOJI_PATTERN.sub("", msg)
        return msg

    def _apply_colors(self, msg, level):
        if self.use_colors:
            color = self.COLOR_MAP.get(level, '')
            return f"{color}{msg}{Style.RESET_ALL}"
        return msg


def configure_logging(
    name: str = "logger",
    path: str = "logs",
    level: int = logging.DEBUG,
    save: bool = False
):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Clear existing handlers to prevent duplication
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(
        EnhancedFormatter(
            "%(asctime)s - %(levelname)s: %(message)s",
            datefmt="%d/%m/%y %H:%M:%S",
            tty_only=True
        )
    )
    logger.addHandler(console_handler)

    # File handler with rotation
    if save:
        logs_dir = Path(path).absolute()
        logs_dir.mkdir(exist_ok=True)

        file_handler = TimedRotatingFileHandler(
            filename=str(logs_dir / f"{datetime.datetime.now().strftime('%d-%m-%Y %H-%M-%S')}.log"),
            when="midnight",
            backupCount=7,
            encoding="utf-8"
        )
        file_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s - %(levelname)s: %(message)s",
                datefmt="%d/%m/%y %H:%M:%S"
            )
        )
        logger.addHandler(file_handler)

    return logger
