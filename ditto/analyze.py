import glob
import json
import os
import re

from genson import SchemaBuilder


def _from_dir(target_dir):
    target_dir = os.path.abspath(target_dir)

    def func_decorator(func):
        def func_wrapper(*args, **kwargs):
            cwd = os.getcwd()
            os.chdir(target_dir)
            result = func(*args, **kwargs)
            os.chdir(cwd)
            return result

        return func_wrapper

    return func_decorator


def do_analyze(data_dir, schema_dir):
    if not os.path.exists(schema_dir):
        os.makedirs(schema_dir)

    @_from_dir(data_dir)
    def get_schema_paths():
        file_names = glob.iglob('**/*.json', recursive=True)
        return sorted({re.sub('/[0-9]+/', '/$id/', file_name) for file_name in file_names})

    @_from_dir(data_dir)
    def gen_single_schema(path):
        glob_exp = path.replace("/$id/", "/*/")
        print(os.path.join(data_dir, glob_exp))
        file_names = glob.iglob(glob_exp, recursive=True)
        schema = SchemaBuilder()
        for file_name in file_names:
            with open(file_name) as f:
                schema.add_object(json.load(f))
        return schema

    @_from_dir(schema_dir)
    def gen_schemas(paths):
        for file_name in paths:
            base_dir = os.path.dirname(file_name)
            if not os.path.exists(base_dir):
                os.makedirs(base_dir)
            schema = gen_single_schema(file_name)
            with open(file_name, 'w') as f:
                f.write(schema.to_json(indent=4, sort_keys=True))

    gen_schemas(get_schema_paths())
