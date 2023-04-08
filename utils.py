from typing import List
from bisect import bisect_left


def binarySearch(li: list, i):
    index = bisect_left(li, i)
    if index != len(li) and li[index] == i:
        return index
    return None
