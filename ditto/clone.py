import json
import os
import os.path
import requests


def do_clone(base_url, target_dir, replacement_url):

    def safe_open_w(file_name):
        os.makedirs(os.path.dirname(file_name), exist_ok=True)
        return open(file_name, "w")

    def print_json(data, file_name):
        transformed_data = json.dumps(data, indent=4, sort_keys=True)
        transformed_data = transformed_data.replace(base_url, replacement_url)
        print(transformed_data, file=safe_open_w(file_name))

    if not base_url.endswith("/"):
        base_url += "/"

    if not target_dir.endswith("/"):
        target_dir += "/"

    # Root

    url = base_url + "api/v2/"
    endpoints = requests.get(url)

    path = target_dir + url.replace(base_url, '') + "index.json"
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
        path = target_dir + endpoint.replace(base_url, '') + "index.json"
        print(path)
        print_json(resource_list.json(), path)

        # All resources
        for resourceSummary in resource_list.json()['results']:
            resource_url = resourceSummary['url']
            path = target_dir + resource_url.replace(base_url, '') + "index.json"

            if not os.path.isfile(path):
                print(path)
                resource = requests.get(resource_url)
                print_json(resource.json(), path)

            if endpoint.endswith("/pokemon/"):
                resource_url += "encounters/"
                path = target_dir + resource_url.replace(base_url, '') + "index.json"
                if not os.path.isfile(path):
                    print(path)
                    resource = requests.get(resource_url)
                    print_json(resource.json(), path)
