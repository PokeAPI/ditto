import glob
import json
import os
import re
from pathlib import Path
from typing import Dict, List, TypeVar

from genson import SchemaBuilder
from tqdm import tqdm

from pokeapi_ditto.commands.models import COMMON_MODELS
from pokeapi_ditto.common import from_path

T = TypeVar("T")


def _replace_common_model(item: T, name: str, model: Dict) -> T:
    if isinstance(item, Dict):
        without_schema = item
        schema = None
        if "$schema" in without_schema:
            without_schema = item.copy()
            schema = without_schema.pop("$schema")
        if without_schema == model:
            result = {"$ref": name}
            if schema:
                result["$schema"] = schema
            return result

        return {k: _replace_common_model(v, name, model) for k, v in item.items()}

    if isinstance(item, List):
        return [_replace_common_model(v, name, model) for v in item]

    return item


def do_analyze(data_dir: str):
    data_path = Path(data_dir)
    api_path = data_path.joinpath("api")
    schema_path = data_path.joinpath("schema")

    if not schema_path.exists():
        schema_path.mkdir(parents=True)

    @from_path(api_path)
    def get_schema_paths() -> List[Path]:
        return sorted(
            {
                Path(*[re.sub("^[0-9]+$", "$id", part) for part in path.parts])
                for path in Path(".").glob("**/*.json")
            }
        )

    @from_path(api_path)
    def gen_single_schema(path: Path) -> SchemaBuilder:
        glob_exp = os.path.join(
            *["*" if part == "$id" else part for part in path.parts]
        )
        file_names = list(glob.iglob(glob_exp, recursive=True))
        schema = SchemaBuilder()
        for file_name in tqdm(file_names, desc=str(path.parent)):
            with open(file_name) as f:
                schema.add_object(json.load(f))
        return schema

    @from_path(schema_path)
    def gen_schemas(paths: List[Path]):
        for path in tqdm(paths):
            if not path.parent.exists():
                os.makedirs(path.parent)
            schema = gen_single_schema(path).to_schema()
            for name, model in COMMON_MODELS.items():
                schema = _replace_common_model(schema, name, model)
            with path.open("w") as f:
                f.write(json.dumps(schema, indent=4, sort_keys=True))

    @from_path(data_path)
    def save_common_schemas():
        for name, model in COMMON_MODELS.items():
            schema_builder = SchemaBuilder()
            schema_builder.add_schema(model)
            schema = schema_builder.to_schema()
            if name.endswith("resource_list.json"):
                schema["properties"]["next"]["type"] = ["null", "string"]
                schema["properties"]["previous"]["type"] = ["null", "string"]
            with Path(name).relative_to(Path(name).root).open("w") as f:
                f.write(json.dumps(schema, indent=4, sort_keys=True))

    gen_schemas(get_schema_paths())
    save_common_schemas()
