from collections import OrderedDict

from odictliteral import odict

# noinspection DuplicatedCode
COMMON_MODELS: OrderedDict = odict[
    "/schema/v2/api_resource.json":{
        "properties": {"url": {"type": "string"}},
        "required": ["url"],
        "type": "object",
    },
    "/schema/v2/named_api_resource.json":{
        "properties": {"name": {"type": "string"}, "url": {"type": "string"}},
        "required": ["name", "url"],
        "type": "object",
    },
    "/schema/v2/api_resource_list.json":{
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
    "/schema/v2/named_api_resource_list.json":{
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
    "/schema/v2/description.json":{
        "properties": {
            "description": {"type": "string"},
            "language": {"$ref": f"/schema/v2/named_api_resource.json"},
        },
        "required": ["description", "language"],
        "type": "object",
    },
    "/schema/v2/effect.json":{
        "properties": {
            "effect": {"type": "string"},
            "language": {"$ref": f"/schema/v2/named_api_resource.json"},
        },
        "required": ["effect", "language"],
        "type": "object",
    },
    "/schema/v2/encounter.json":{
        "properties": {
            "chance": {"type": "integer"},
            "condition_values": {
                "items": {"$ref": f"/schema/v2/named_api_resource.json"},
                "type": "array",
            },
            "max_level": {"type": "integer"},
            "method": {"$ref": f"/schema/v2/named_api_resource.json"},
            "min_level": {"type": "integer"},
        },
        "required": ["chance", "condition_values", "max_level", "method", "min_level"],
        "type": "object",
    },
    "/schema/v2/flavor_text.json":{
        "properties": {
            "flavor_text": {"type": "string"},
            "language": {"$ref": f"/schema/v2/named_api_resource.json"},
        },
        "required": ["flavor_text", "language"],
        "type": "object",
    },
    "/schema/v2/generation_game_index.json":{
        "properties": {
            "game_index": {"type": "integer"},
            "generation": {"$ref": f"/schema/v2/named_api_resource.json"},
        },
        "required": ["game_index", "generation"],
        "type": "object",
    },
    "/schema/v2/machine_version_detail.json":{
        "properties": {
            "machine": {"$ref": f"/schema/v2/api_resource.json"},
            "version_group": {"$ref": f"/schema/v2/named_api_resource.json"},
        },
        "required": ["machine", "version_group"],
        "type": "object",
    },
    "/schema/v2/name.json":{
        "properties": {
            "language": {"$ref": f"/schema/v2/named_api_resource.json"},
            "name": {"type": "string"},
        },
        "required": ["language", "name"],
        "type": "object",
    },
    "/schema/v2/verbose_effect.json":{
        "properties": {
            "effect": {"type": "string"},
            "language": {"$ref": f"/schema/v2/named_api_resource.json"},
            "short_effect": {"type": "string"},
        },
        "required": ["effect", "language", "short_effect"],
        "type": "object",
    },
    "/schema/v2/version_encounter_detail.json":{
        "properties": {
            "encounter_details": {
                "items": {"$ref": "/schema/v2/encounter.json"},
                "type": "array",
            },
            "max_chance": {"type": "integer"},
            "version": {"$ref": "/schema/v2/named_api_resource.json"},
        },
        "required": ["encounter_details", "max_chance", "version"],
        "type": "object",
    },
    "/schema/v2/version_game_index.json":{
        "properties": {
            "game_index": {"type": "integer"},
            "version": {"$ref": f"/schema/v2/named_api_resource.json"},
        },
        "required": ["game_index", "version"],
        "type": "object",
    },
    "/schema/v2/version_group_flavor_text.json":{
        "properties": {
            "language": {"$ref": "/schema/v2/named_api_resource.json"},
            "text": {"type": "string"},
            "version_group": {"$ref": "/schema/v2/named_api_resource.json"},
        },
        "required": ["language", "text", "version_group"],
        "type": "object",
    },
]
