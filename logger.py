#!/usr/bin/env python3
import datetime
import logging
import re
import sys
import tarfile
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
    r"\U00010000-\U0010ffff"
    r"]+",
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

    def __init__(self, fmt: str, datefmt: Optional[str] = None, tty_only: bool = True):
        super().__init__(fmt, datefmt)
        self.tty_only = tty_only
        self.use_colors = sys.stdout.isatty() or not tty_only

    def format(self, record):
        msg = super().format(record)
        msg = self._process_special_chars(msg)
        return self._apply_colors(msg, record.levelno)

    def _process_special_chars(self, msg):
        # Replace special characters
        msg = msg.replace("\u2192", "-->")
        if any(ord(c) > 0x7F for c in msg):
            return EMOJI_PATTERN.sub("", msg)
        return msg

    def _apply_colors(self, msg, level):
        if self.use_colors:
            color = self.COLOR_MAP.get(level, '')
            return f"{color}{msg}{Style.RESET_ALL}"
        return msg


def archive_old_logs(logs_dir: Path, current_log_file: Path) -> None:
    """
    Archive any existing log files (except the one that is newly created)
    into a tar.gz file and then remove those log files.
    """
    old_logs = [log_file for log_file in logs_dir.glob("*.log") if log_file != current_log_file]
    if not old_logs:
        return

    archive_name = logs_dir / f"logs_archive_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.tar.gz"
    with tarfile.open(archive_name, "w:gz") as tar:
        for log_file in old_logs:
            tar.add(log_file, arcname=log_file.name)

    for log_file in old_logs:
        try:
            log_file.unlink()
        except Exception as err:
            print(f"Error deleting log file {log_file}: {err}", file=sys.stderr)


def configure_logging(
    name: str = "logger",
    path: str = "logs",
    level: int = logging.DEBUG,
    save: bool = False
):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Remove existing handlers to avoid duplicate logs.
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # Set up the console handler.
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(
        EnhancedFormatter(
            "%(asctime)s - %(levelname)s: %(message)s",
            datefmt="%d/%m/%y %H:%M:%S",
            tty_only=True
        )
    )
    logger.addHandler(console_handler)

    if save:
        # Ensure the log directory exists.
        logs_dir = Path(path).absolute()
        logs_dir.mkdir(parents=True, exist_ok=True)

        # Create a new unique log file name using the current timestamp.
        new_log_filename = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S") + ".log"
        new_log_file = logs_dir / new_log_filename

        # Archive all previous log files that are not the current one.
        archive_old_logs(logs_dir, new_log_file)

        # Set up a file handler that rotates at midnight.
        file_handler = TimedRotatingFileHandler(
            filename=str(new_log_file),
            when="midnight",
            backupCount=7,
            encoding="utf-8"
        )
        file_handler.setFormatter(logging.Formatter(
            "%(asctime)s - %(levelname)s: %(message)s",
            datefmt="%d/%m/%y %H:%M:%S"
        ))
        logger.addHandler(file_handler)

    return logger
