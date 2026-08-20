import re


def apply_base_url(data: str, base_url: str) -> str:
    return re.sub(r'(")(/(api|schema)/v2)', r"\1{0}\2".format(base_url), data)
