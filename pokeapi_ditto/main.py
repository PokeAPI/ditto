import argparse
import importlib.metadata
import sys
from typing import Any

from pokeapi_ditto.commands import analyze, clone, transform


class Ditto(object):
    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "--version",
            action="version",
            version=importlib.metadata.version("pokeapi-ditto"),
        )
        subparsers = parser.add_subparsers(dest="command")

        clone_args = subparsers.add_parser("clone")
        clone_args.add_argument("--src-url", type=str, default="http://localhost/")
        clone_args.add_argument("--dest-dir", type=str, default="./data")
        clone_args.add_argument("--select", nargs="+", default=[])
        clone_args.add_argument(
            "--max-workers",
            type=int,
            default=None,
            help="Max concurrent worker threads (or set DITTO_MAX_WORKERS env var)",
        )

        transform_args = subparsers.add_parser("transform")
        transform_args.add_argument("--src-dir", type=str, default="./data")
        transform_args.add_argument("--dest-dir", type=str, default="./dist")
        transform_args.add_argument("--base-url", type=str, required=True)

        analyze_args = subparsers.add_parser("analyze")
        analyze_args.add_argument("--data-dir", type=str, default="./data")

        args = vars(parser.parse_args(sys.argv[1:]))
        command = args.pop("command")
        if command is None:
            parser.print_help()
            exit(1)

        print(
            "Doing '{}' with configuration: {}".format(command, args), file=sys.stderr
        )
        getattr(self, command)(args)

    @staticmethod
    def clone(args: Any):
        clone.do_clone(**args)

    @staticmethod
    def transform(args: Any):
        transform.do_transform(**args)

    @staticmethod
    def analyze(args: Any):
        analyze.do_analyze(**args)


def main():
    Ditto()
