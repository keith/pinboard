import argparse
import signal
import sys

from . import __version__
from . import add
from . import cleanup
from . import open_urls


def _signal_handle(sig, frame):
    sys.exit(0)


def _build_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--version", action="version",
                        version="%(prog)s " + __version__)

    subparsers = parser.add_subparsers(dest="subcommand")
    subparsers.required = True

    add_parser = subparsers.add_parser("add", help="Add a URL to read")
    add_parser.add_argument("url", help="the URL to add to pinboard")

    open_parser = subparsers.add_parser(
        "open", help="Open and delete some unread URLs"
    )
    open_parser.add_argument("count", help="the number of URLs", type=int)

    subparsers.add_parser(
        "cleanup", help="Prompting to delete URLs with a failed status code"
    )

    return parser


def main():
    args = _build_parser().parse_args()
    commands = {
        "add": add.main,
        "cleanup": cleanup.main,
        "open": open_urls.main,
    }

    signal.signal(signal.SIGINT, _signal_handle)
    commands[args.subcommand](args)
