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
    print('Usage: ' + sys.argv[0] + ' <baseUrl> <targetDir>', file=sys.stderr)
    quit(1)

baseUrl = sys.argv[1]
targetDir = sys.argv[2]

if not baseUrl.endswith("/"):
    baseUrl += "/"

if not targetDir.endswith("/"):
    targetDir += "/"

# Root

url = baseUrl + "api/v2/"
endpoints = requests.get(url)

path = targetDir + url.replace(baseUrl, '') + "index.json"
print(path)
print_json(endpoints.json(), path)

# Endpoints

for endpoint in endpoints.json().values():
    # Default index
    url = endpoint
    resource_list = requests.get(url)
    path = targetDir + endpoint.replace(baseUrl, '') + "index.json"
    print(path)
    print_json(resource_list.json(), path)

    # Fifty index
    url = endpoint + "?limit=50"
    resource_list = requests.get(url)
    path = targetDir + endpoint.replace(baseUrl, '') + "limit=50.json"
    print(path)
    print_json(resource_list.json(), path)

    # Zero index
    url = endpoint + "?limit=0"
    resource_list = requests.get(url)
    path = targetDir + endpoint.replace(baseUrl, '') + "limit=0.json"
    print(path)
    print_json(resource_list.json(), path)

    # All index
    count = str(resource_list.json()["count"])
    url = endpoint + "?limit=" + count
    resource_list = requests.get(url)
    path = targetDir + endpoint.replace(baseUrl, '') + "limit=" + count + ".json"
    print(path)
    print_json(resource_list.json(), path)

    # All resources
    for resourceSummary in resource_list.json()['results']:
        resourceUrl = resourceSummary['url']
        path = targetDir + resourceUrl.replace(baseUrl, '') + "index.json"

        if not os.path.isfile(path):
            print(path)
            resource = requests.get(resourceUrl)
            print_json(resource.json(), path)

        if endpoint.endswith("/pokemon/"):
            resourceUrl += "encounters/"
            path = targetDir + resourceUrl.replace(baseUrl, '') + "index.json"
            if not os.path.isfile(path):
                print(path)
                resource = requests.get(resourceUrl)
                print_json(resource.json(), path)
