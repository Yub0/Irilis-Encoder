"""qBittorrent API wrapper."""

# Third Party
from qbittorrentapi import Client

# First Party
from encoder.dataclass import (
    SettingsqBittorrent,
    Torrent,
    TorrentCategory,
    TorrentFile,
    TorrentTag,
)
from encoder.exceptions import qBittorrentNotLogged, qBittorrentTorrentNotFound


class qBittorrent:
    """qBittorrent API wrapper."""

    def __init__(self, settings_qbittorrent: SettingsqBittorrent) -> None:
        """
        Initialize qBittorrent API wrapper.

        Args:
            settings_qbittorrent (SettingsqBittorrent): The qBittorrent
                settings.
        """
        self._client = Client(host=settings_qbittorrent.url)

    def _check_logged_in(self) -> None:
        """
        Check if the client is logged in and raise an exception if not.

        Raises:
            qBittorrentNotLogged: If qBittorrent is not logged in.
        """
        if not self._client.is_logged_in:
            raise qBittorrentNotLogged(
                "qBittorrent is not logged in. Please check credentials."
            )

    def _serialize_torrent(self, torrents: dict | list[dict]) -> Torrent:
        """
        Serialize torrent.

        Args:
            torrents (dict | list[dict]): The torrent data to serialize.

        Returns:
            Torrent: A serialized Torrent object.
        """
        if isinstance(torrents, dict):
            torrents = [torrents]

        for torrent in torrents:
            category = TorrentCategory(torrent.category)
            tags = [TorrentTag(name=tag) for tag in torrent.tags]
            files = [
                TorrentFile(name=file.name, size=file.size)
                for file in torrent.files
            ]

            return Torrent(
                name=torrent.name,
                hash=torrent.hash,
                category=category,
                tags=tags,
                files=files,
                path=torrent.save_path,
                progression=int(torrent.progress * 100),
            )

    def get_torrents(self) -> list[Torrent]:
        """
        Return list of torrents.

        Returns:
            list[Torrent]: List of torrents.
        """
        self._check_logged_in()
        torrents = self._client.torrents.info()
        return [
            self._serialize_torrent(torrent)
            for torrent in [
                torrent for torrent in torrents if torrent.category
            ]
        ]

    def get_torrent(self, hash: str) -> Torrent:
        """
        Return torrent (using dataclasses).

        Args:
            hash (str): Torrent hash.

        Raises:
            qBittorrentTorrentNotFound: If torrent is not found.

        Returns:
            Torrent: Torrent.
        """
        self._check_logged_in()
        torrent = self._client.torrents.info(hash=hash)[0]

        if not torrent:
            raise qBittorrentTorrentNotFound(
                f"Torrent with hash {hash} not found."
            )
        return self._serialize_torrent(torrent)

    def add_tags(self, hash: str, tags: str | list[str]) -> None:
        """
        Add tags to torrent.

        Args:
            hash (str): Torrent hash.
            tags (str | list[str]): Tags to add to torrent.
        """
        self._check_logged_in()
        if isinstance(tags, str):
            tags = [tags]
        self._client.torrents_add_tags(tags=tags, torrent_hashes=hash)
