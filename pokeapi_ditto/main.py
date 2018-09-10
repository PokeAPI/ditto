import argparse
import sys

from gevent.pywsgi import WSGIServer

from pokeapi_ditto import __version__
from pokeapi_ditto.commands import analyze, clone, serve, transform


class Ditto(object):
    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--version", action="version", version=__version__)
        subparsers = parser.add_subparsers(dest="command")

        clone_args = subparsers.add_parser("clone")
        clone_args.add_argument("--src-url", type=str, default="http://localhost/")
        clone_args.add_argument("--dest-dir", type=str, default="./data")

        transform_args = subparsers.add_parser("transform")
        transform_args.add_argument("--src-dir", type=str, default="./data")
        transform_args.add_argument("--dest-dir", type=str, default="./dist")
        transform_args.add_argument("--base-url", type=str, required=True)

        analyze_args = subparsers.add_parser("analyze")
        analyze_args.add_argument("--api-dir", type=str, default="./data/api")
        analyze_args.add_argument("--schema-dir", type=str, default="./data/schema")

        serve_args = subparsers.add_parser("serve")
        serve_args.add_argument("--port", type=int, default=80)
        serve_args.add_argument("--base-url", type=str, default="")
        serve_args.add_argument("--root-dir", type=str, default="./data")

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
    def clone(args):
        clone.do_clone(**args)

    @staticmethod
    def transform(args):
        transform.do_transform(**args)

    @staticmethod
    def analyze(args):
        analyze.do_analyze(**args)

    @staticmethod
    def serve(args):
        port = args.pop("port")
        app = serve.create_app(**args)
        WSGIServer(("", port), app).serve_forever()


if __name__ == "__main__":
    Ditto()
