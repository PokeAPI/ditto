from pathlib import Path
from typing import Any, Dict

import orjson
from tqdm import tqdm

from pokeapi_ditto.common import apply_base_url


def _is_id(s: str) -> bool:
    try:
        int(s)
        return True
    except ValueError:
        return False


def _dump(path: Path, content: Any) -> None:
    if not path.parent.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(orjson.dumps(content, option=orjson.OPT_INDENT_2))


# TODO: blow all this up and make it good
# this is really bade code and hard to follow
# all this path.parent.parent nonsense is hard to understand
# clone.py is a cleaner model to follow


def do_transform(src_dir: str, dest_dir: str, base_url: str) -> None:
    src_dir_path = Path(src_dir)
    dest_dir_path = Path(dest_dir)

    if base_url.endswith("/"):
        base_url = base_url[:-1]

    if not dest_dir_path.exists():
        dest_dir_path.mkdir(parents=True, exist_ok=True)

    src_files = list(src_dir_path.glob("**/*.json"))

    for file_path in tqdm(src_files):
        content: Dict[str, Any] = orjson.loads(
            apply_base_url(file_path.read_text(), base_url)
        )

        # all files
        dest_file = dest_dir_path.joinpath(file_path.relative_to(src_dir_path))
        _dump(dest_file, content)

        # named resource files
        if _is_id(dest_file.parent.name) and "name" in content:
            name = content["name"]
            named_dest_file = dest_file.parent.parent.joinpath(name, "index.json")
            _dump(named_dest_file, content)

        # a hack for pokemon/ID/encounters
        if (
            _is_id(dest_file.parent.parent.name)
            and dest_file.parent.name == "encounters"
        ):
            pokemon_path = file_path.parent.parent.joinpath("index.json")
            name = orjson.loads(pokemon_path.read_bytes())["name"]
            enc_dest_file = dest_file.parent.parent.parent.joinpath(
                name, "encounters", "index.json"
            )
            _dump(enc_dest_file, content)
