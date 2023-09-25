"""Encoder main module."""

# Standard Library
from threading import Thread

# Third Party
import click
from dotenv import load_dotenv

# First Party
from encoder.daemon import Daemon
from encoder.dataclass import Settings, SettingsqBittorrent
from encoder.logger import EncoderLogger

load_dotenv()


@click.command()
@click.option(
    "--fast-qbittorrent-url",
    envvar="FAST_QBITTORRENT_URL",
    help="URL of the fast qBittorrent.",
    required=True,
)
@click.option(
    "--fast-qbittorrent-host",
    envvar="FAST_QBITTORRENT_HOST",
    help="Host of the fast qBittorrent.",
    required=True,
)
@click.option(
    "--fast-qbittorrent-port",
    envvar="FAST_QBITTORRENT_PORT",
    help="Port of the fast qBittorrent.",
    required=True,
)
@click.option(
    "--fast-qbittorrent-username",
    envvar="FAST_QBITTORRENT_USERNAME",
    help="Username of the fast qBittorrent.",
    required=True,
)
@click.option(
    "--fast-qbittorrent-password",
    envvar="FAST_QBITTORRENT_PASSWORD",
    help="Password of the fast qBittorrent.",
    required=True,
)
@click.option(
    "--slow-qbittorrent-url",
    envvar="SLOW_QBITTORRENT_URL",
    help="URL of the slow qBittorrent.",
    required=True,
)
@click.option(
    "--slow-qbittorrent-host",
    envvar="SLOW_QBITTORRENT_HOST",
    help="Host of the slow qBittorrent.",
    required=True,
)
@click.option(
    "--slow-qbittorrent-port",
    envvar="SLOW_QBITTORRENT_PORT",
    help="Port of the slow qBittorrent.",
    required=True,
)
@click.option(
    "--slow-qbittorrent-username",
    envvar="SLOW_QBITTORRENT_USERNAME",
    help="Username of the slow qBittorrent.",
    required=True,
)
@click.option(
    "--slow-qbittorrent-password",
    envvar="SLOW_QBITTORRENT_PASSWORD",
    help="Password of the slow qBittorrent.",
    required=True,
)
def main(
    fast_qbittorrent_url: str,
    fast_qbittorrent_host: str,
    fast_qbittorrent_port: int,
    fast_qbittorrent_username: str,
    fast_qbittorrent_password: str,
    slow_qbittorrent_url: str,
    slow_qbittorrent_host: str,
    slow_qbittorrent_port: int,
    slow_qbittorrent_username: str,
    slow_qbittorrent_password: str,
) -> None:
    """
    Run the encoder in a thread.

    Args:
        fast_qbittorrent_url (str): URL of the fast qBittorrent.
        fast_qbittorrent_host (str): Host of the fast qBittorrent.
        fast_qbittorrent_port (int): Port of the fast qBittorrent.
        fast_qbittorrent_username (str): Username of the fast qBittorrent.
        fast_qbittorrent_password (str): Password of the fast qBittorrent.
        slow_qbittorrent_url (str): URL of the slow qBittorrent.
        slow_qbittorrent_host (str): Host of the slow qBittorrent.
        slow_qbittorrent_port (int): Port of the slow qBittorrent.
        slow_qbittorrent_username (str): Username of the slow qBittorrent.
        slow_qbittorrent_password (str): Password of the slow qBittorrent.
    """
    settings = Settings(
        fast_qbittorrent=SettingsqBittorrent(
            url=fast_qbittorrent_url,
            host=fast_qbittorrent_host,
            port=fast_qbittorrent_port,
            username=fast_qbittorrent_username,
            password=fast_qbittorrent_password,
        ),
        slow_qbittorrent=SettingsqBittorrent(
            url=slow_qbittorrent_url,
            host=slow_qbittorrent_host,
            port=slow_qbittorrent_port,
            username=slow_qbittorrent_username,
            password=slow_qbittorrent_password,
        ),
    )
    encoder_logger = EncoderLogger()

    exit(
        Thread(
            target=Daemon(
                encoder_logger=encoder_logger, settings=settings
            ).run()
        )
    )
