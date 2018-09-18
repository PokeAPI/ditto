import json
import os
from multiprocessing import Pool
from pathlib import Path
from signal import SIG_IGN, SIGINT, signal
from typing import Any, Callable, List, Tuple

import requests
from tqdm import tqdm
from yarl import URL


def _do_in_parallel(worker: Callable, data: List, desc: str) -> None:
    cpus = os.cpu_count()
    pool = Pool(cpus, initializer=lambda: signal(SIGINT, SIG_IGN))
    try:
        for _ in tqdm(pool.imap_unordered(worker, data), total=len(data), desc=f"{desc} ({cpus}x)"):
            pass
    except KeyboardInterrupt as interrupt:
        pool.terminate()
        pool.join()
        raise interrupt


class Cloner:

    _src_url: URL
    _dest_dir: Path

    def __init__(self, src_url: str, dest_dir: str):
        if src_url.endswith("/"):
            src_url = src_url[:-1]
        if not dest_dir.endswith("/"):
            dest_dir += "/"

        self._src_url = URL(src_url)
        self._dest_dir = Path(dest_dir)

    def _crawl(self, url: URL, save: bool = True) -> Any:
        try:
            data = requests.get(url).json()
        except json.JSONDecodeError as err:
            tqdm.write(f"JSON decode failure: {url}")
            return None

        if save:
            out_data = json.dumps(data, indent=4, sort_keys=True)
            out_data = out_data.replace(str(self._src_url), "")
            file = self._dest_dir.joinpath((url / "index.json").path[1:])
            file.parent.mkdir(parents=True, exist_ok=True)
            file.write_text(out_data)

        return data

    def _crawl_index(self) -> List[URL]:
        index = self._crawl(self._src_url / "api/v2")
        return [URL(url_str) for url_str in index.values()]

    def _crawl_resource_list(self, url: URL) -> List[URL]:
        zero_url = url.with_query({"limit": 0, "offset": 0})
        count = self._crawl(zero_url, save=False)["count"]
        full_url = url.with_query({"limit": count, "offset": 0})
        resource_list = self._crawl(full_url)
        return [URL(resource_ref["url"]) for resource_ref in resource_list["results"]]

    def clone_single(self, endpoint_and_id: Tuple[str, str]) -> None:
        endpoint, id = endpoint_and_id
        res_url = self._src_url / "api/v2" / endpoint / id
        self._crawl(res_url)
        if endpoint == "pokemon":
            self._crawl(res_url / "encounters")

    def clone_endpoint(self, endpoint: str):
        res_list_url = self._src_url / "api/v2" / endpoint
        res_urls = self._crawl_resource_list(res_list_url)
        singles = [(endpoint, url.parent.name) for url in res_urls]
        _do_in_parallel(
            worker=self.clone_single,
            data=singles,
            desc=res_list_url.name,
        )

    def clone_all(self) -> None:
        resource_lists = self._crawl_index()
        for res_list_url in tqdm(resource_lists, desc="clone"):
            endpoint = res_list_url.parent.name
            self.clone_endpoint(endpoint)


def do_clone(src_url: str, dest_dir: str, select: List[str]) -> None:
    cloner = Cloner(src_url, dest_dir)

    if not select:
        cloner.clone_all()

    for sel in select:
        if "/" in sel:
            cloner.clone_single(tuple(filter(None, sel.split("/")))[0:2])
        else:
            cloner.clone_endpoint(sel)
