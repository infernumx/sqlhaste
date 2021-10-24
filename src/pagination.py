from itertools import zip_longest
from typing import Any


def grouper(iterable, n, fillvalue=None):
    "Collect data into non-overlapping fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


class Paginator:
    def __init__(self, data, console):
        self.data = data
        self.page = 0

    def get_page(self, page: int) -> list[Any]:
        pass
