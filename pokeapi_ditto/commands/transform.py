import json
from pathlib import Path
from typing import Dict, Any

from tqdm import tqdm

from pokeapi_ditto.common import apply_base_url


def _is_id(s: str):
    try:
        int(s)
        return True
    except ValueError:
        return False


def _dump(path: Path, content: Any):
    if not path.parent.exists():
        path.parent.mkdir(parents=True)
    path.write_text(json.dumps(content, sort_keys=True, indent=4))


# TODO: blow all this up and make it good
# this is really bade code and hard to follow
# all this path.parent.parent nonsense is hard to understand
# clone.py is a cleaner model to follow


def do_transform(src_dir: str, dest_dir: str, base_url: str):
    src_dir: Path = Path(src_dir)
    dest_dir: Path = Path(dest_dir)

    if base_url.endswith("/"):
        base_url = base_url[:-1]

    if not dest_dir.exists():
        dest_dir.mkdir(parents=True)

    src_paths = src_dir.glob("**/*.json")

    for src_path in tqdm(list(src_paths)):
        content: Dict = json.loads(apply_base_url(src_path.read_text(), base_url))

        # all files
        dest_path = dest_dir.joinpath(src_path.relative_to(src_dir))
        _dump(dest_path, content)

        # named resource files
        if _is_id(dest_path.parent.name) and "name" in content:
            name = content["name"]
            dest_path = dest_path.parent.parent.joinpath(name, "index.json")
            _dump(dest_path, content)

        # a hack for pokemon/ID/encounters
        if (
            _is_id(dest_path.parent.parent.name)
            and dest_path.parent.name == "encounters"
        ):
            pokemon_path = src_path.parent.parent.joinpath("index.json")
            name = json.loads(pokemon_path.read_text())["name"]
            dest_path = dest_path.parent.parent.parent.joinpath(
                name, "encounters", "index.json"
            )
            _dump(dest_path, content)
