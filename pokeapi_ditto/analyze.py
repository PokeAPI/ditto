import glob
import json
import os
import re
from pathlib import Path, PurePath
from typing import List

from genson import SchemaBuilder


def _from_dir(target_dir: str):
    target_dir = os.path.abspath(target_dir)

    def func_decorator(func: callable):
        def func_wrapper(*args, **kwargs):
            cwd = os.getcwd()
            os.chdir(target_dir)
            result = func(*args, **kwargs)
            os.chdir(cwd)
            return result

        return func_wrapper

    return func_decorator


def do_analyze(data_dir: str, schema_dir: str):
    if not Path(schema_dir).exists():
        Path(schema_dir).mkdir(parents=True)

    @_from_dir(data_dir)
    def get_schema_paths() -> List[Path]:
        return sorted(
            {
                Path(*[re.sub("^[0-9]+$", "$id", part) for part in path.parts])
                for path in Path(".").glob("**/*.json")
            }
        )

    @_from_dir(data_dir)
    def gen_single_schema(path: Path) -> SchemaBuilder:
        glob_exp = os.path.join(
            *["*" if part == "$id" else part for part in path.parts]
        )
        print(os.path.join(*Path(data_dir).parts, glob_exp))
        file_names = glob.iglob(glob_exp, recursive=True)
        schema = SchemaBuilder()
        for file_name in file_names:
            with open(file_name) as f:
                schema.add_object(json.load(f))
        return schema

    @_from_dir(schema_dir)
    def gen_schemas(paths: List[Path]):
        for path in paths:
            if not path.parent.exists():
                os.makedirs(path.parent)
            schema = gen_single_schema(path)
            with path.open("w") as f:
                f.write(schema.to_json(indent=4, sort_keys=True))

    gen_schemas(get_schema_paths())
