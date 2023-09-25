"""Encoder main module."""

# Standard Library
from threading import Thread, exit

# Third Party
import click

# First Party
from encoder.daemon import Daemon
from encoder.dataclass import Settings


@click.command()
@click.option(
    "--fast-qbittorrent-url",
    envvar="FAST_QBITTORRENT_URL",
    help="URL of the fast qBittorrent.",
    required=True,
)
@click.option(
    "--slow-qbittorrent-url",
    envvar="SLOW_QBITTORRENT_URL",
    help="URL of the slow qBittorrent.",
    required=True,
)
def main(fast_qbittorrent_url: str, slow_qbittorrent_url: str) -> None:
    """
    Run the encoder in a thread.

    Args:
        fast_qbittorrent_url (str): URL of the fast qBittorrent.
        slow_qbittorrent_url (str): URL of the slow qBittorrent.
    """
    settings = Settings(
        fast_qbittorrent_url=fast_qbittorrent_url,
        slow_qbittorrent_url=slow_qbittorrent_url,
    )

    exit(Thread(target=Daemon(settings=settings).run()))
