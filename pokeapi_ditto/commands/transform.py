import json
from pathlib import Path
from typing import Dict

from tqdm import tqdm

from pokeapi_ditto.common import apply_base_url


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

        dest_path = dest_dir.joinpath(src_path.relative_to(src_dir))

        if not dest_path.parent.exists():
            dest_path.parent.mkdir(parents=True)
        dest_path.write_text(json.dumps(content, sort_keys=True, indent=4))

        if "name" in content and "id" in content:
            name = content["name"]
            dest_path = dest_path.parent.parent.joinpath(name, "index.json")

            if not dest_path.parent.exists():
                dest_path.parent.mkdir(parents=True)
            dest_path.write_text(json.dumps(content, sort_keys=True, indent=4))
