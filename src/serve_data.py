import sys
import re
import json
from flask import Flask, url_for, request

# Config

if len(sys.argv) != 3:
    print('Usage: ' + sys.argv[0] + ' <port> <data_dir>', file=sys.stderr)
    quit(1)

port = int(sys.argv[1])
data_dir = sys.argv[2]

if not data_dir.endswith("/"):
    data_dir += "/"

# Serve

app = Flask(__name__)
app.url_map.strict_slashes = False


def get_api_resource(path):
    original = open(data_dir + 'api/v2/' + path + '/index.json', 'r').read()
    replaced = re.sub('http://[a-zA-Z0-9.]+/', url_for('root', _external=True), original)
    return replaced


def safe_cast(val, to_type, default=None):
    try:
        return to_type(val)
    except (TypeError, ValueError):
        return default


# noinspection PyUnusedLocal
@app.errorhandler(FileNotFoundError)
@app.errorhandler(404)
def not_found(error):
    return '{"error": "Not found"}', 404


@app.route('/')
def root():
    return '{"information": "https://github.com/pokesource/ditto"}'


@app.route('/api/v2/')
def index():
    return get_api_resource('')


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

    return json.dumps(result_obj, indent=4, sort_keys=True)


@app.route('/api/v2/<string:category>/<int:key>/')
def resource(category, key):
    return get_api_resource("%s/%s" % (category, key))


@app.route('/api/v2/<string:category>/<int:key>/<string:extra>/')
def resource_extra(category, key, extra):
    return get_api_resource('%s/%s/%s' % (category, key, extra))


app.run(port=port)
