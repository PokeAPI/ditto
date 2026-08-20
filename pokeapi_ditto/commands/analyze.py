import glob
import os
import re
from pathlib import Path
from typing import Dict, List, TypeVar

import orjson
from genson import SchemaBuilder
from tqdm import tqdm

from pokeapi_ditto.commands.models import COMMON_MODELS

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

    def get_schema_paths() -> List[Path]:
        return sorted(
            {
                Path(
                    *[
                        re.sub("^[0-9]+$", "$id", part)
                        for part in path.relative_to(api_path).parts
                    ]
                )
                for path in api_path.glob("**/*.json")
            }
        )

    def gen_single_schema(path: Path) -> SchemaBuilder:
        glob_exp = str(
            api_path
            / os.path.join(*["*" if part == "$id" else part for part in path.parts])
        )
        file_names = list(glob.iglob(glob_exp, recursive=True))
        schema = SchemaBuilder()
        for file_name in tqdm(file_names, desc=str(path.parent)):
            with open(file_name, "rb") as f:
                schema.add_object(orjson.loads(f.read()))
        return schema

    def gen_schemas(paths: List[Path]):
        for path in tqdm(paths):
            out_path = schema_path / path
            out_path.parent.mkdir(parents=True, exist_ok=True)
            schema = gen_single_schema(path).to_schema()
            for name, model in COMMON_MODELS.items():
                schema = _replace_common_model(schema, name, model)
            out_path.write_bytes(orjson.dumps(schema, option=orjson.OPT_INDENT_2))

    def save_common_schemas():
        for name, model in COMMON_MODELS.items():
            schema_builder = SchemaBuilder()
            schema_builder.add_schema(model)
            schema = schema_builder.to_schema()
            if name.endswith("resource_list.json"):
                schema["properties"]["next"]["type"] = ["null", "string"]
                schema["properties"]["previous"]["type"] = ["null", "string"]
            out_file = data_path / Path(name).relative_to(Path(name).root)
            out_file.parent.mkdir(parents=True, exist_ok=True)
            out_file.write_bytes(orjson.dumps(schema, option=orjson.OPT_INDENT_2))

    gen_schemas(get_schema_paths())
    save_common_schemas()
