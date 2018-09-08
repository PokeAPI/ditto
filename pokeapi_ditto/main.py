import argparse
import sys

from gevent.pywsgi import WSGIServer

from pokeapi_ditto import analyze, clone, serve


class Ditto(object):
    def __init__(self):
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers(dest="command")

        clone_args = subparsers.add_parser("clone")
        clone_args.add_argument("--source", type=str, default="http://localhost/")
        clone_args.add_argument("--destination", type=str, default="./data")
        clone_args.add_argument(
            "--replacement-url", type=str, default="https://pokeapi.co/"
        )

        serve_args = subparsers.add_parser("serve")
        serve_args.add_argument("--port", type=int, default=80)

        analyze_args = subparsers.add_parser("analyze")
        analyze_args.add_argument("--api-dir", type=str, default="./data/api")
        analyze_args.add_argument("--schema-dir", type=str, default="./data/schema")

        args = parser.parse_args(sys.argv[1:])
        if args.command is None:
            parser.print_help()
            exit(1)
        getattr(self, args.command)(args)

    @staticmethod
    def analyze(args):
        analyze.do_analyze(args.api_dir, args.schema_dir)

    @staticmethod
    def clone(args):
        clone.do_clone(args.source, args.destination, args.replacement_url)

    @staticmethod
    def serve(args):
        print("Starting Ditto server with configuration: {}".format(vars(args)))
        WSGIServer(("", args.port), serve.app).serve_forever()
