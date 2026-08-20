import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any, Callable, List, NamedTuple, Tuple

import orjson
import requests
from requests.adapters import HTTPAdapter
from tqdm import tqdm
from urllib3.util.retry import Retry
from yarl import URL


class RequestTimeout(NamedTuple):
    connect: int
    read: int


_REQUEST_TIMEOUT = RequestTimeout(connect=5, read=30)


def _calculate_max_workers() -> int:
    """
    Derive client thread count from co-located server capacity.

    https://github.com/PokeAPI/pokeapi/blob/master/gunicorn.conf.py

    Assumes both this client and the target server run on the same machine,
    and the server uses gunicorn's default worker formula: 2 * cpu_count.
    We target 1.5x the server's worker count to keep the request pipeline
    saturated (accounting for network/IO round-trip slack) without starving
    the server of CPU time. Capped at 24 to bound memory and fd usage.
    """
    cpu = os.cpu_count() or 4
    server_workers = 2 * cpu  # gunicorn default: 2 * CPU count
    client_threads = int(server_workers * 1.5)  # 1.5x to fill the pipeline
    return min(max(4, client_threads), 24)


_MAX_WORKERS = _calculate_max_workers()


def _do_in_parallel(
    worker: Callable[[Tuple[str, str]], None], data: List[Tuple[str, str]], desc: str
) -> None:
    with ThreadPoolExecutor(max_workers=_MAX_WORKERS) as executor:
        futures = [executor.submit(worker, item) for item in data]
        try:
            for future in tqdm(
                as_completed(futures),
                total=len(futures),
                desc=f"{desc} ({_MAX_WORKERS}T)",
                mininterval=1,
                position=1,
                leave=False,
            ):
                future.result()
        except KeyboardInterrupt:
            executor.shutdown(wait=False, cancel_futures=True)
            raise


class Cloner:

    _src_url: URL
    _dest_dir: Path
    _session: requests.Session

    def __init__(self, src_url: str, dest_dir: str):
        if src_url.endswith("/"):
            src_url = src_url[:-1]
        if not dest_dir.endswith("/"):
            dest_dir += "/"

        self._src_url = URL(src_url)
        self._dest_dir = Path(dest_dir)
        self._session = self._build_session()

    @staticmethod
    def _build_session() -> requests.Session:
        session = requests.Session()
        retry = Retry(
            total=3,
            backoff_factor=0.5,
            status_forcelist=[500, 502, 503, 504],
            allowed_methods=["GET"],
        )
        adapter = HTTPAdapter(
            pool_connections=_MAX_WORKERS,
            pool_maxsize=_MAX_WORKERS,
            max_retries=retry,
        )
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session

    def _crawl(self, url: URL, save: bool = True) -> Any:
        try:
            response = self._session.get(str(url), timeout=_REQUEST_TIMEOUT)
            response.raise_for_status()
            data = orjson.loads(response.content)
        except requests.RequestException as e:
            tqdm.write(f"Request failure: {url} ({e})")
            return None
        except orjson.JSONDecodeError:
            tqdm.write(f"JSON decode failure: {url}")
            return None

        if save:
            out_data = orjson.dumps(data, option=orjson.OPT_INDENT_2)
            src_url_bytes = str(self._src_url).encode("utf-8")
            out_data = out_data.replace(src_url_bytes, b"")
            file = self._dest_dir.joinpath((url / "index.json").path[1:])
            file.parent.mkdir(parents=True, exist_ok=True)
            file.write_bytes(out_data)

        return data

    def _crawl_index(self) -> List[URL]:
        index = self._crawl(self._src_url / "api/v2")
        return [URL(url_str) for url_str in index.values()]

    def _crawl_resource_list(self, url: URL) -> List[URL]:
        zero_url = url.with_query({"limit": 0, "offset": 0})
        payload = self._crawl(zero_url, save=False)
        if "count" in payload:
            count = payload["count"]
            full_url = url.with_query({"limit": count, "offset": 0})
            resource_list = self._crawl(full_url)
            return [
                URL(resource_ref["url"]) for resource_ref in resource_list["results"]
            ]
        else:
            self._crawl(url)
            return []

    def clone_single(self, endpoint_and_id: Tuple[str, str]) -> None:
        endpoint, id = endpoint_and_id
        res_url = URL("{}/api/v2/{}/{}/".format(self._src_url, endpoint, id))
        self._crawl(res_url)
        if endpoint == "pokemon":
            self._crawl(URL("{}encounters/".format(res_url)))

    def clone_endpoint(self, endpoint: str):
        res_list_url = self._src_url / "api/v2" / endpoint
        res_urls = self._crawl_resource_list(res_list_url)
        singles = [(endpoint, url.parent.name) for url in res_urls]
        _do_in_parallel(worker=self.clone_single, data=singles, desc=res_list_url.name)

    def clone_all(self) -> None:
        resource_lists = self._crawl_index()
        for res_list_url in tqdm(resource_lists, desc="clone", position=0):
            endpoint = res_list_url.parent.name
            self.clone_endpoint(endpoint)


def do_clone(src_url: str, dest_dir: str, select: List[str]) -> None:
    cloner = Cloner(src_url, dest_dir)

    if not select:
        cloner.clone_all()

    for sel in select:
        if "/" in sel:
            cloner.clone_single(
                tuple(filter(None, sel.split("/")))[0:2]  # pyright: ignore[reportArgumentType]
            )
        else:
            cloner.clone_endpoint(sel)
