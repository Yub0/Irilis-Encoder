"""Dataclasses for the encoder."""

# Standard Library
from enum import Enum

# Third Party
from pydantic import BaseModel


class Settings(BaseModel):
    """Encoder settings."""

    fast_qbittorrent_url: str
    slow_qbittorrent_url: str


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


class Torrent(BaseModel):
    """A torrent."""

    name: str
    hash: str
    category: TorrentCategory
    tags: list[TorrentTag] = []
    files: list[TorrentFile] = []
    progression: int
