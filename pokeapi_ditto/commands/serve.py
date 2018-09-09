import json

from flask import Flask, Response, request, url_for
from flask_cors import CORS

from pokeapi_ditto import __version__
from pokeapi_ditto.common import apply_base_url


def _to_json(obj):
    return json.dumps(obj, indent=4, sort_keys=True)


def _safe_cast(val, to_type, default=None):
    try:
        return to_type(val)
    except (TypeError, ValueError):
        return default


class DittoApp:
    def __init__(self, root_dir: str, base_url: str):
        if not root_dir.endswith("/"):
            root_dir += "/"
        self.root_dir = root_dir

        if base_url.endswith("/"):
            base_url = base_url[:-1]
        self.base_url = base_url

    def _stream_file(self, file):
        for line in file:
            yield apply_base_url(line, self.base_url)

    def api_path(self, path: str):
        return self.root_dir + "api/v2/" + path + "/index.json"

    def streamed_api_file(self, path: str):
        return self._stream_file(open(self.api_path(path)))

    def get_index(self):
        return self.streamed_api_file(".")

    def get_resource_list(self, category: str):
        result_obj = json.loads(open(self.api_path(category)).read())

        args = request.args.to_dict()
        offset = max(_safe_cast(args.get("offset"), int, 0), 0)
        limit = _safe_cast(args.get("limit"), int, 20)

        result_obj["results"] = result_obj["results"][offset : offset + limit]
        if offset > 0:
            prev_offset = max(offset - limit, 0)
            prev_page = url_for(
                "resource_list",
                category=category,
                limit=limit,
                offset=prev_offset,
                _external=True,
            )
            result_obj["previous"] = prev_page
        if offset + limit < result_obj["count"]:
            next_offset = offset + limit
            next_page = url_for(
                "resource_list",
                category=category,
                limit=limit,
                offset=next_offset,
                _external=True,
            )
            result_obj["next"] = next_page

        return apply_base_url(_to_json(result_obj), self.base_url)

    def get_resource_item(self, category: str, key: str):
        return self.streamed_api_file("/".join([category, key]))

    def get_resource_extra(self, category: str, key: str, extra: str):
        return self.streamed_api_file("/".join([category, key, extra]))


def create_app(root_dir: str, base_url: str):
    app = Flask(__name__)
    CORS(app)
    app.url_map.strict_slashes = False

    ditto = DittoApp(root_dir, base_url)

    content_json = "application/json"

    @app.errorhandler(FileNotFoundError)
    @app.errorhandler(404)
    def not_found_404(_):
        return Response(
            _to_json({"error": "Not found"}), status=404, mimetype=content_json
        )

    @app.errorhandler(500)
    def not_found_500(_):
        return Response(
            _to_json({"error": "Internal server error"}),
            status=500,
            mimetype=content_json,
        )

    @app.route("/")
    def root():
        return Response(
            _to_json({"application": "pokeapi-ditto", "version": __version__}),
            status=200,
            mimetype=content_json,
        )

    @app.route("/api/v2/")
    def index():
        return Response(ditto.get_index(), status=200, mimetype=content_json)

    @app.route("/api/v2/<string:category>/")
    def resource_list(category):
        return Response(
            ditto.get_resource_list(category), status=200, mimetype=content_json
        )

    @app.route("/api/v2/<string:category>/<string:key>/")
    def resource_item(category, key):
        return Response(
            ditto.get_resource_item(category, key), status=200, mimetype=content_json
        )

    @app.route("/api/v2/<string:category>/<string:key>/<string:extra>")
    def resource_extra(category, key, extra):
        return Response(
            ditto.get_resource_extra(category, key, extra),
            status=200,
            mimetype=content_json,
        )

    return app
