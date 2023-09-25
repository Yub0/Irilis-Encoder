"""Logger module."""
# Standard Library
import sys
from typing import Optional

# Third Party
from loguru import logger as loguru_logger


class EncoderLogger:
    """Encoder logger."""

    def __init__(self, log_file: Optional[str] = "encoder.log") -> None:
        """
        Initialize the encoder logger.

        Args:
            log_file (str, optional): The path to the log file. Defaults to
                "encoder.log".
        """
        self.log_file = log_file

        loguru_logger.remove()
        loguru_logger.add(sys.stderr, level="INFO")
        loguru_logger.add(self.log_file, rotation="10 MB", level="DEBUG")

    def info(self, message: str) -> None:
        """
        Log info message.

        Args:
            message (str): The message to log.
        """
        loguru_logger.info(message)

    def debug(self, message: str) -> None:
        """
        Log debug message.

        Args:
            message (str): The message to log.
        """
        loguru_logger.debug(message)

    def warning(self, message: str) -> None:
        """
        Log warning message.

        Args:
            message (str): The message to log.
        """
        loguru_logger.warning(message)

    def error(self, message: str) -> None:
        """
        Log error message.

        Args:
            message (str): The message to log.
        """
        loguru_logger.error(message)

    def exception(self, message: str) -> None:
        """
        Log exception message.

        Args:
            message (str): The message to log.
        """
        loguru_logger.exception(message)
