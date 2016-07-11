import re
import json
import os
from flask import *
from flask_cors import CORS


def build(data_dir):
    if not data_dir.endswith("/"):
        data_dir += "/"

    app = Flask(__name__)
    CORS(app)
    app.url_map.strict_slashes = False

    def get_api_resource(path):
        original = open(data_dir + 'api/v2/' + path + '/index.json', 'r').read()
        replaced = re.sub('http://[a-zA-Z0-9.]+/', url_for('root', _external=True), original)
        return replaced
        
    def get_media_resource(path):
        return open(data_dir + 'media/' + path, 'r+b').read()

    def safe_cast(val, to_type, default=None):
        try:
            return to_type(val)
        except (TypeError, ValueError):
            return default

    # noinspection PyUnusedLocal
    @app.errorhandler(FileNotFoundError)
    def not_found_file(error):
        return '{"error": "File not found"}', 404, {'Content-Type': 'application/json'}

    # noinspection PyUnusedLocal
    @app.errorhandler(404)
    def not_found_404(error):
        return '{"error": "Not found"}', 404, {'Content-Type': 'application/json'}

    @app.route('/')
    def root():
        return '{"information": "https://github.com/pokesource/ditto"}', 200, {'Content-Type': 'application/json'}

    @app.route('/media/<path:path>')
    def media(path):
        return get_media_resource(path), 200, {'Content-Type': 'image/png'}

    @app.route('/api/v2/')
    def index():
        return get_api_resource(''), 200, {'Content-Type': 'application/json'}

    @app.route('/api/v2/<string:category>/')
    def resource_list(category):
        result_obj = json.loads(get_api_resource(category))

        args = request.args.to_dict()
        offset = max(safe_cast(args.get('offset'), int, 0), 0)
        limit = safe_cast(args.get('limit'), int, 20)

        result_obj['results'] = result_obj['results'][offset:offset + limit]
        if offset > 0:
            url = url_for('resource_list', category=category, limit=limit, offset=max(offset - limit, 0), _external=True)
            result_obj['previous'] = url
        if offset + limit < result_obj['count']:
            url = url_for('resource_list', category=category, limit=limit, offset=offset + limit, _external=True)
            result_obj['next'] = url

        return json.dumps(result_obj, indent=4, sort_keys=True), 200, {'Content-Type': 'application/json'}

    @app.route('/api/v2/<string:category>/<int:key>/')
    def resource(category, key):
        return get_api_resource("%s/%s" % (category, key)), 200, {'Content-Type': 'application/json'}

    @app.route('/api/v2/<string:category>/<int:key>/<string:extra>/')
    def resource_extra(category, key, extra):
        return get_api_resource('%s/%s/%s' % (category, key, extra)), 200, {'Content-Type': 'application/json'}

    return app
