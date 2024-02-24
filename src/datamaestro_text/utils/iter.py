from typing import Callable, TypeVar, Iterator, List, Union

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


class FactoryIterable:
    def __init__(self, factory: Callable[[], Iterator[T]]):
        self.factory: Callable[[], Iterator[T]] = factory

    def __iter__(self) -> Iterator[T]:
        return self.factory()


class RangeView:
    def __init__(self, source, key: Union[slice, range]):
        self.key = (
            key if isinstance(key, range) else range(key.start, key.stop, key.step)
        )
        self.source = source

    def __getitem__(self, key: Union[slice, int]):
        slice = self.range[key]

        if isinstance(slice, int):
            return self.source[slice]

        return RangeView(self.source, key)


class LazyList:
    """Iterable-based list

    The list is only materialized if needed"""

    def __init__(self, iterable, materialize_threshold=0):
        self.iterable = iterable
        self.materialized_list = None
        self.materialize_threshold = materialize_threshold

    def __iter__(self):
        # If not materialized, return an iterator over the iterable
        if self.materialized_list is None:
            return iter(self.iterable)
        # If materialized, return an iterator over the materialized list
        else:
            return iter(self.materialized_list)

    def __getitem__(self, index):
        # Materialize the list if accessing an index above the threshold or any slice
        if isinstance(index, slice) or index >= self.materialize_threshold:
            self._materialize()
        elif self.materialized_list is None:
            # Returns the element at the given index
            return [
                element for _, element in zip(range(index + 1), iter(self.iterable))
            ][-1]

        return self.materialized_list[index]

    def _materialize(self):
        # Convert the iterable to a list if it hasn't been already
        if self.materialized_list is None:
            self.materialized_list = list(self.iterable)
