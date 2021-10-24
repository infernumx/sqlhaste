from itertools import zip_longest
from typing import Any


def grouper(iterable, n, fillvalue=None):
    "Collect data into non-overlapping fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


class Paginator:
    def __init__(self, data: list[Any], size: int):
        self.data: list[Any] = data
        self.size: int = size
        self.paged: list[list[Any]] = list(grouper(data, size))

    def get_pages(self) -> int:
        return len(self.paged)

    def get_page(
        self,
        page: int,
    ) -> list[Any]:
        return self.paged[page]
