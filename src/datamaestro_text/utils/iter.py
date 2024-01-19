from typing import TypeVar, Iterator, List

T = TypeVar("T")


class BatchIterator(Iterator[List[T]]):
    """Adapter for iterators to return batches of elements instead of"""

    def __init__(self, iterator: Iterator[T], size: int):
        self.iterator = iterator
        self.size = size

    def __next__(self):
        batch = []
        for _, element in zip(range(self.size), self.iterator):
            batch.append(element)

        if len(batch) == 0:
            raise StopIteration()

        return batch
