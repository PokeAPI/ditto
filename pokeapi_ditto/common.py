import os

BASE_URL_PLACEHOLDER = "$BASE_URL_PLACEHOLDER"


def from_dir(target_dir: str) -> callable:
    target_dir = os.path.abspath(target_dir)

    def func_decorator(func: callable) -> callable:
        def func_wrapper(*args, **kwargs):
            cwd = os.getcwd()
            os.chdir(target_dir)
            result = func(*args, **kwargs)
            os.chdir(cwd)
            return result

        return func_wrapper

    return func_decorator


def apply_base_url(data: str, base_url: str) -> str:
    return data.replace(BASE_URL_PLACEHOLDER, base_url)
