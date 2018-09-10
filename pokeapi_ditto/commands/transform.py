from pathlib import Path
from typing import Iterable

from tqdm import tqdm

from pokeapi_ditto.common import apply_base_url


def do_transform(src_dir: str, dest_dir: str, base_url: str):
    src_dir: Path = Path(src_dir)
    dest_dir: Path = Path(dest_dir)

    if base_url.endswith("/"):
        base_url = base_url[:-1]

    if not dest_dir.exists():
        dest_dir.mkdir(parents=True)

    orig_paths: Iterable[Path] = src_dir.glob("api/**/*.json")

    for orig in tqdm(list(orig_paths)):
        new = dest_dir.joinpath(orig.relative_to(src_dir))

        if not new.parent.exists():
            new.parent.mkdir(parents=True)

        new.write_text(apply_base_url(orig.read_text(), base_url))
