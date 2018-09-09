import glob
import json
import os
import re
from pathlib import Path
from typing import List

from genson import SchemaBuilder

from pokeapi_ditto.common import from_dir


def do_analyze(api_dir: str, schema_dir: str, log: bool):
    if not Path(schema_dir).exists():
        Path(schema_dir).mkdir(parents=True)

    @from_dir(api_dir)
    def get_schema_paths() -> List[Path]:
        return sorted(
            {
                Path(*[re.sub("^[0-9]+$", "$id", part) for part in path.parts])
                for path in Path(".").glob("**/*.json")
            }
        )

    @from_dir(api_dir)
    def gen_single_schema(path: Path) -> SchemaBuilder:
        glob_exp = os.path.join(
            *["*" if part == "$id" else part for part in path.parts]
        )
        file_names = glob.iglob(glob_exp, recursive=True)
        schema = SchemaBuilder()
        for file_name in file_names:
            with open(file_name) as f:
                schema.add_object(json.load(f))
        return schema

    @from_dir(schema_dir)
    def gen_schemas(paths: List[Path]):
        for path in paths:
            if log:
                print(Path(schema_dir).joinpath(path))
            if not path.parent.exists():
                os.makedirs(path.parent)
            schema = gen_single_schema(path)
            with path.open("w") as f:
                f.write(schema.to_json(indent=4, sort_keys=True))

    gen_schemas(get_schema_paths())
