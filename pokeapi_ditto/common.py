import os
from pathlib import Path


def from_path(target_path: Path) -> callable:
    target_path = target_path.absolute()

    def func_decorator(func: callable) -> callable:
        def func_wrapper(*args, **kwargs):
            cwd = os.getcwd()
            os.chdir(str(target_path))
            result = func(*args, **kwargs)
            os.chdir(cwd)
            return result

        return func_wrapper

    return func_decorator


def apply_base_url(data: str, base_url: str) -> str:
    return data.replace(BASE_URL_PLACEHOLDER, base_url)
