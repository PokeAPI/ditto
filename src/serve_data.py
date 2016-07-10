import sys
from flask import Flask

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
    return original


@app.errorhandler(FileNotFoundError)
@app.errorhandler(404)
def not_found(error):
    return '{"error": "Not found"}', 404


@app.route('/api/v2/')
def index():
    return get_api_resource('')


@app.route('/api/v2/<string:category>/')
def resource_list(category):
    return get_api_resource(category)


@app.route('/api/v2/<string:category>/<key>/')
def resource(category, key):
    return get_api_resource("%s/%s" % (category, key))


@app.route('/api/v2/<string:category>/<key>/<string:extra>/')
def resource_extra(category, key, extra):
    return get_api_resource("%s/%s/%s" % (category, key, extra))


if __name__ == '__main__':
    app.run(port=port)
