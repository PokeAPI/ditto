from ditto import app, clone
import argparse
import sys
from gevent.wsgi import WSGIServer


class Ditto(object):

    def __init__(self):
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers(dest='command')

        transform = subparsers.add_parser('clone')
        transform.add_argument('--source', type=str, default='http://localhost/')
        transform.add_argument('--destination', type=str, default='./data')
        transform.add_argument('--replacement-url', type=str, default='https://pokeapi.co/')

        serve = subparsers.add_parser('serve')
        serve.add_argument('--port', type=int, default=80)

        args = parser.parse_args(sys.argv[1:])
        if args.command is None:
            parser.print_help()
            exit(1)
        getattr(self, args.command)(args)

    @staticmethod
    def clone(args):
        clone.do_clone(args.source, args.destination, args.replacement_url)

    @staticmethod
    def serve(args):
        print('Starting Ditto server with configuration: {}'.format(vars(args)))
        WSGIServer(('', args.port), app.app).serve_forever()
