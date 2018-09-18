from collections import OrderedDict

from odictliteral import odict

COMMON_MODELS: OrderedDict = odict[
    f"/schema/v2/api_resource.json":{
        "properties": {"url": {"type": "string"}},
        "required": ["url"],
        "type": "object",
    },
    f"/schema/v2/named_api_resource.json":{
        "properties": {"name": {"type": "string"}, "url": {"type": "string"}},
        "required": ["name", "url"],
        "type": "object",
    },
    f"/schema/v2/api_resource_list.json":{
        "properties": {
            "count": {"type": "integer"},
            "next": {"type": "null"},
            "previous": {"type": "null"},
            "results": {
                "items": {"$ref": f"/schema/v2/api_resource.json"},
                "type": "array",
            },
        },
        "required": ["count", "next", "previous", "results"],
        "type": "object",
    },
    f"/schema/v2/named_api_resource_list.json":{
        "properties": {
            "count": {"type": "integer"},
            "next": {"type": "null"},
            "previous": {"type": "null"},
            "results": {
                "items": {"$ref": f"/schema/v2/named_api_resource.json"},
                "type": "array",
            },
        },
        "required": ["count", "next", "previous", "results"],
        "type": "object",
    },
]
