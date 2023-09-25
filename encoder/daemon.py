"""Daemon module."""

# First Party
from encoder.dataclass import Settings
from encoder.datasources.downloader import Downloader
from encoder.datasources.qbittorrent import qBittorrent
from encoder.logger import EncoderLogger


class Daemon:
    """Daemon class."""

    def __init__(
        self, encoder_logger: EncoderLogger, settings: Settings
    ) -> None:
        """
        Initialize Irilis Encoder daemon.

        Args:
            encoder_logger (EncoderLogger): The encoder logger.
            settings (Settings): The settings of the encoder.
        """
        self.encoder_logger = encoder_logger
        self.settings = settings
        self.downloader = Downloader(
            self.encoder_logger,
            self.settings.fast_qbittorrent,
        )

    def run(self) -> None:
        """Run the daemon."""
        print(f"fast_qbittorrent_url: {self.settings.fast_qbittorrent.url}")
        print(f"slow_qbittorrent_url: {self.settings.slow_qbittorrent.url}")

        torrents_to_transcode = qBittorrent(
            self.settings.fast_qbittorrent,
        ).get_torrents()

        if not torrents_to_transcode:
            self.encoder_logger.info("No torrents to transcode.")
            return

        self.encoder_logger.info(
            f"Found {len(torrents_to_transcode)} torrent(s) to transcode."
        )

        torrent_to_transcode = torrents_to_transcode[0]
        self.encoder_logger.info(
            "Selected torrent to transcode: {}. Containing {} file(s).".format(
                torrent_to_transcode.name,
                len(torrent_to_transcode.files),
            )
        )

        sample_files = [
            file
            for file in torrent_to_transcode.files
            if file.size < 150000000 and "sample" in file.name.lower()
        ]

        if sample_files:
            self.encoder_logger.info(
                f"Found {len(sample_files)} sample file(s) to remove."
            )
            torrent_to_transcode.files = [
                file
                for file in torrent_to_transcode.files
                if file not in sample_files
            ]

        for file in torrent_to_transcode.files:
            self.downloader.download_file(file)
