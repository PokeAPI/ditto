import json
import re

from flask import *
from flask_cors import CORS


def to_json(obj):
    return json.dumps(obj, indent=4, sort_keys=True)


def replace_host(string, url):
    return re.sub('http://[a-zA-Z0-9.]+/', url, string)


def safe_cast(val, to_type, default=None):
    try:
        return to_type(val)
    except (TypeError, ValueError):
        return default


def stream_file(file, url):
    for line in file:
        yield replace_host(line, url)


def host_url():
    return url_for('root', _external=True)


class DittoApp:

    def __init__(self, root_dir: str):
        if not root_dir.endswith('/'):
            root_dir += '/'
        self.root_dir = root_dir

    def api_path(self, path: str):
        return self.root_dir + 'api/v2/' + path + '/index.json'

    def media_path(self, path: str):
        return self.root_dir + 'media/' + path

    def streamed_api_file(self, path: str):
        return stream_file(open(self.api_path(path)), host_url())

    def get_index(self):
        return self.streamed_api_file('.')

    def get_resource_list(self, category: str):
        result_obj = json.loads(open(self.api_path(category)).read())

        args = request.args.to_dict()
        offset = max(safe_cast(args.get('offset'), int, 0), 0)
        limit = safe_cast(args.get('limit'), int, 20)

        result_obj['results'] = result_obj['results'][offset:offset + limit]
        if offset > 0:
            prev_offset = max(offset - limit, 0)
            prev_page = url_for('resource_list', category=category, limit=limit, offset=prev_offset, _external=True)
            result_obj['previous'] = prev_page
        if offset + limit < result_obj['count']:
            next_offset = offset + limit
            next_page = url_for('resource_list', category=category, limit=limit, offset=next_offset, _external=True)
            result_obj['next'] = next_page

        return replace_host(to_json(result_obj), host_url())

    def get_resource_item(self, category: str, key: str):
        return self.streamed_api_file(category + '/' + key)

    def get_resource_extra(self, category: str, key: str, extra: str):
        return self.streamed_api_file(category + '/' + key + '/' + extra)

    def get_media(self, path: str):
        return open(self.media_path(path), 'r+b').read()


app = Flask(__name__)
CORS(app)
app.url_map.strict_slashes = False

ditto = DittoApp('./data')

error_404 = to_json({
    'error': 'Not found'
})

error_500 = to_json({
    'error': 'Internal server error'
})

information = to_json({
    'git_repo': 'https://github.com/pokesource/ditto.git',
    'docker': 'pokesource/ditto',
    'github': 'pokesource/ditto'
})

content_json = 'application/json'
content_png = 'image/png'


@app.errorhandler(FileNotFoundError)
@app.errorhandler(404)
def not_found_404(_):
    return Response(error_404, status=404, mimetype=content_json)


@app.errorhandler(500)
def not_found_500(_):
    return Response(error_500, status=500, mimetype=content_json)


@app.route('/')
def root():
    return Response(information, status=200, mimetype=content_json)


@app.route('/media/<path:path>')
def media(path):
    return Response(ditto.get_media(path), status=200, mimetype=content_png)


@app.route('/api/v2/')
def index():
    return Response(ditto.get_index(), status=200, mimetype=content_json)


@app.route('/api/v2/<string:category>/')
def resource_list(category):
    return Response(ditto.get_resource_list(category), status=200, mimetype=content_json)


@app.route('/api/v2/<string:category>/<string:key>/')
def resource_item(category, key):
    return Response(ditto.get_resource_item(category, key), status=200, mimetype=content_json)


@app.route('/api/v2/<string:category>/<string:key>/<string:extra>')
def resource_extra(category, key, extra):
    return Response(ditto.get_resource_extra(category, key, extra), status=200, mimetype=content_json)
