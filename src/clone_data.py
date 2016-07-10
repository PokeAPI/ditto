#!/usr/bin/env python3

import json
import os
import os.path
import requests
import sys


def safe_open_w(file_name):
    os.makedirs(os.path.dirname(file_name), exist_ok=True)
    return open(file_name, "w")


def print_json(data, file_name):
    print(json.dumps(data, indent=4, sort_keys=True), file=safe_open_w(file_name))


# Config

if len(sys.argv) != 3:
    print('Usage: ' + sys.argv[0] + ' <base_url> <target_dir>', file=sys.stderr)
    quit(1)

base_url = sys.argv[1]
target_dir = sys.argv[2]

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
        resourceUrl = resourceSummary['url']
        path = target_dir + resourceUrl.replace(base_url, '') + "index.json"

        if not os.path.isfile(path):
            print(path)
            resource = requests.get(resourceUrl)
            print_json(resource.json(), path)

        if endpoint.endswith("/pokemon/"):
            resourceUrl += "encounters/"
            path = target_dir + resourceUrl.replace(base_url, '') + "index.json"
            if not os.path.isfile(path):
                print(path)
                resource = requests.get(resourceUrl)
                print_json(resource.json(), path)
