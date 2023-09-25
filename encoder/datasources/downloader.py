"""Downloader module."""

# Standard Library
import os

# Third Party
from paramiko import AutoAddPolicy, SSHClient

# First Party
from encoder.dataclass import SettingsqBittorrent, TorrentFile
from encoder.logger import EncoderLogger


class Downloader:
    """Downloader class."""

    def __init__(
        self,
        encoder_logger: EncoderLogger,
        settings_qbittorrent: SettingsqBittorrent,
    ) -> None:
        """
        Initialize Downloader.

        Args:
            encoder_logger (EncoderLogger): The encoder logger.
            settings_qbittorrent (SettingsqBittorrent): The qBittorrent
                settings.
        """
        self.client = SSHClient()
        self.client.set_missing_host_key_policy(AutoAddPolicy())
        self.encoder_logger = encoder_logger
        self.settings_qbittorrent = settings_qbittorrent

        # Automatically connect to SSH when an instance is created
        self._connect()

    def _connect(self) -> None:
        """Connect to the remote server."""
        try:
            self.client.connect(
                hostname=self.settings_qbittorrent.host,
                port=self.settings_qbittorrent.port,
                username=self.settings_qbittorrent.username,
                password=self.settings_qbittorrent.password,
            )
            self.encoder_logger.info("Connected to SSH.")
        except Exception as e:
            self.encoder_logger.error(f"Error connecting to SSH: {e}")

    def download_file(self, file: TorrentFile) -> None:
        """
        Download a file from the remote server.

        Args:
            file (TorrentFile): The torrent file to download.
        """
        try:
            sftp = self.client.open_sftp()
            local_path = os.path.join(os.getcwd(), file.name.split("/")[-1])

            # Check if file already exists locally using the file size
            if os.path.exists(local_path) and (
                os.path.getsize(local_path) == file.size
            ):
                self.encoder_logger.info(
                    f"File {file.name} already downloaded."
                )
                return

            self.encoder_logger.info(f"Downloading file: {local_path}")
            sftp.get(file.name, local_path)
            sftp.close()
            self.encoder_logger.info(f"Downloaded file: {local_path}")
        except Exception as e:
            self.encoder_logger.error(f"Error downloading file: {e}")
