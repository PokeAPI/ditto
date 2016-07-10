import app
import clone
import argparse
import sys


class Ditto(object):

    def __init__(self):
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers(dest='command')

        transform = subparsers.add_parser('capture')
        transform.add_argument('--source', type=str, default='http://localhost/')
        transform.add_argument('--destination', type=str, default='./data')

        serve = subparsers.add_parser('transform')
        serve.add_argument('--port', type=int, default=80)
        serve.add_argument('--source', type=str, default='./data')

        args = parser.parse_args(sys.argv[1:])
        if args.command is None:
            parser.print_help()
            exit(1)
        getattr(self, args.command)(args)

    @staticmethod
    def capture(args):
        clone.do_clone(args.source, args.destination)

    @staticmethod
    def transform(args):
        app.build(args.source).run(port=args.port)

if __name__ == '__main__':
    Ditto()
