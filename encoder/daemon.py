"""Daemon module."""

# First Party
from encoder.dataclass import Settings


class Daemon:
    """Daemon class."""

    def __init__(self, settings: Settings) -> None:
        """
        Initialize Irilis Encoder daemon.

        Args:
            settings (Settings): The settings of the encoder.
        """
        self.settings = settings

    def run(self) -> None:
        """Run the daemon."""
        print(f"fast_qbittorrent_url: {self.settings.fast_qbittorrent_url}")
        print(f"slow_qbittorrent_url: {self.settings.slow_qbittorrent_url}")
