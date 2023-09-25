"""Exceptions for the encoder."""


class qBittorrentNotLogged(Exception):
    """Exception raised when the client is not logged in."""


class qBittorrentTorrentNotFound(Exception):
    """Exception raised when the torrent is not found."""
