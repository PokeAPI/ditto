import json
import os
import os.path

import requests

from pokeapi_ditto.common import BASE_URL_PLACEHOLDER


def do_clone(src_url: str, dest_dir: str, log: bool):
    if not src_url.endswith("/"):
        src_url += "/"

    if not dest_dir.endswith("/"):
        dest_dir += "/"

    def safe_open_w(file_name):
        os.makedirs(os.path.dirname(file_name), exist_ok=True)
        return open(file_name, "w")

    def print_json(data, file_name):
        transformed_data = json.dumps(data, indent=4, sort_keys=True)
        transformed_data = transformed_data.replace(src_url, BASE_URL_PLACEHOLDER + "/")
        print(transformed_data, file=safe_open_w(file_name))

    # Root

    url = src_url + "api/v2/"
    endpoints = requests.get(url)

    path = dest_dir + url.replace(src_url, "") + "index.json"
    if log:
        print(path)
    print_json(endpoints.json(), path)

    # Endpoints

    for endpoint in endpoints.json().values():
        # Zero index
        url = endpoint + "?limit=0"
        resource_list = requests.get(url)
        count = str(resource_list.json()["count"])

        # Full index
        url = endpoint + "?limit=" + count
        resource_list = requests.get(url)
        path = dest_dir + endpoint.replace(src_url, "") + "index.json"
        if log:
            print(path)
        print_json(resource_list.json(), path)

        # All resources
        for resourceSummary in resource_list.json()["results"]:
            resource_url = resourceSummary["url"]
            path = dest_dir + resource_url.replace(src_url, "") + "index.json"

            if not os.path.isfile(path):
                print(path)
                resource = requests.get(resource_url)
                print_json(resource.json(), path)

            if endpoint.endswith("/pokemon/"):
                resource_url += "encounters/"
                path = dest_dir + resource_url.replace(src_url, "") + "index.json"
                if not os.path.isfile(path):
                    print(path)
                    resource = requests.get(resource_url)
                    print_json(resource.json(), path)
