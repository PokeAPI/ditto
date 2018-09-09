from pathlib import Path
from typing import List

from pokeapi_ditto.common import apply_base_url


def do_transform(src_dir: str, dest_dir: str, base_url: str, log: bool):
    src_dir: Path = Path(src_dir)
    dest_dir: Path = Path(dest_dir)

    if base_url.endswith("/"):
        base_url = base_url[:-1]

    if not dest_dir.exists():
        dest_dir.mkdir(parents=True)

    orig_paths: List[Path] = src_dir.glob("api/**/*.json")

    for orig in orig_paths:
        new = dest_dir.joinpath(orig.relative_to(src_dir))
        if log:
            print(new)

        if not new.parent.exists():
            new.parent.mkdir(parents=True)

        new.write_text(apply_base_url(orig.read_text(), base_url))
