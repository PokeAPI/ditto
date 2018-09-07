import glob
import re
import os
import json
from genson import SchemaBuilder

def _from_dir(dir):
    dir = os.path.abspath(dir)
    def func_decorator(func):
        def func_wrapper(*args, **kwargs):
            cwd = os.getcwd()
            os.chdir(dir)
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
        filenames = glob.iglob('**/*.json', recursive=True)
        return sorted({re.sub('\/[0-9]+\/', '/$id/', filename) for filename in filenames})

    @_from_dir(data_dir)
    def gen_single_schema(path):
        globexp = path.replace("/$id/", "/*/")
        print(os.path.join(data_dir, globexp))
        filenames = glob.iglob(globexp, recursive=True)
        schema = SchemaBuilder()
        for filename in filenames:
            with open(filename) as f:
                schema.add_object(json.load(f))
        return schema

    @_from_dir(schema_dir)
    def gen_schemas(paths):
        for filename in paths:
            basedir = os.path.dirname(filename)
            if not os.path.exists(basedir):
                os.makedirs(basedir)
            schema = gen_single_schema(filename)
            with open(filename, 'w') as f:
                f.write(schema.to_json(indent=4, sort_keys=True))

    gen_schemas(get_schema_paths())
