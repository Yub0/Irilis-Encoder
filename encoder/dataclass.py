"""Dataclasses for the encoder."""

# Standard Library
from enum import Enum

# Third Party
from pydantic import BaseModel


class SettingsqBittorrent(BaseModel):
    """Encoder settings for qBittorrent."""

    url: str
    host: str
    port: int
    username: str
    password: str


class Settings(BaseModel):
    """Encoder settings."""

    fast_qbittorrent: SettingsqBittorrent
    slow_qbittorrent: SettingsqBittorrent


class TorrentCategory(str, Enum):
    """A torrent category."""

    MOVIE = "movie"
    TV = "tv"


class TorrentTag(BaseModel):
    """A torrent tag."""

    name: str


class TorrentFile(BaseModel):
    """A torrent file."""

    name: str
    size: int


class Torrent(BaseModel):
    """A torrent."""

    name: str
    hash: str
    category: TorrentCategory
    tags: list[TorrentTag] = []
    files: list[TorrentFile] = []
    progression: int
    path: str
