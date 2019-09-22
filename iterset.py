"""Set operations on sorted iterables."""

__all__ = [
    "merge",
    "includes",
    "issubset",
    "issuperset",
    "union",
    "intersection",
    "difference",
    "symmetric_difference",
]


class _peekable:
    _sentinel = object()

    def __init__(self, iterable):
        self._it = iter(iterable)
        self._cache = self._sentinel

    def __iter__(self):
        return self

    def __bool__(self):
        try:
            self.peek()
        except StopIteration:
            return False
        return True

    def peek(self):
        if self._cache is self._sentinel:
            self._cache = next(self._it)
        return self._cache

    def __next__(self):
        if self._cache is not self._sentinel:
            result, self._cache = self._cache, self._sentinel
            return result
        return next(self._it)


def _keyify(a, key):
    if key is None:
        return _peekable((x, x) for x in a)
    else:
        return _peekable((x, key(x)) for x in a)


def merge(a, b, key=None):
    """merge(a, b, key=None) -> all elements in a and all elements in b,
    merged in sorted order according to key. If the key function is not
    specified or is none, the element itself is used for comparison. As
    with groupby, the iterables need to be already sorted according to
    the key function. Unlike union, an element that appears in both
    inputs will appear twice in the output.
    """
    a, b = _keyify(a, key), _keyify(b, key)
    while a and b:
        x, kx = a.peek()
        y, ky = b.peek()
        if kx < ky:
            yield x
            next(a)
        else:
            yield y
            next(b)
    yield from (x for (x, kx) in a)
    yield from (y for (y, ky) in b)


def includes(a, b, key=None):
    """includes(a, b, key=None) -> true if a includes all elements from
    b. If the key function is not specified or is none, the element
    itself is used for comparison. As with groupby, the iterables need
    to be already sorted according to the key function. Duplicates
    within b must appear a corresponding number of times in a.
    """
    a, b = _keyify(a, key), _keyify(b, key)
    while b:
        if not a:
            return False
        x, kx = a.peek()
        y, ky = b.peek()
        if ky < kx:
            return False
        elif kx < ky:
            next(b)
        next(a)
    return True


def issubset(a, b, key=None):
    """issubset(a, b, key=None) -> true if b includes all elements from
    a. If the key function is not specified or is none, the element
    itself is used for comparison. As with groupby, the iterables need
    to be already sorted according to the key function. Duplicates
    within a must appear a corresponding number of times in b.
    """
    return includes(b, a, key)

def issuperset(a, b, key=None):
    """issuperset(a, b, key=None) -> true if a includes all elements
    from b. If the key function is not specified or is none, the element
    itself is used for comparison. As with groupby, the iterables need
    to be already sorted according to the key function. Duplicates
    within a must appear b corresponding number of times in a.
    """
    return includes(, b, key)


def union(a, b, key=None):
    """union(a, b, key=None) -> all elements in either a or b, in sorted
    order according to key. If the key function is not specified or is
    none, the element itself is used for comparison. As with groupby,
    the iterables need to be already sorted according to the key
    function. Unlike merge, an element that appears in both inputs will
    appear only once in the output. However, duplicates within either
    iterable will be retained.
    """
    a, b = _keyify(a, key), _keyify(b, key)
    while a and b:
        x, kx = a.peek()
        y, ky = b.peek()
        if kx < ky:
            yield x
            next(a)
        elif ky < kx:
            yield y
            next(b)
        else:
            yield x
            next(a)
            next(b)
    yield from (x for (x, kx) in a)
    yield from (y for (y, ky) in b)


def intersection(a, b, key=None):
    """intersection(a, b, key=None) -> all elements in both a and b, in
    sorted order according to key. If the key function is not specified
    or is none, the element itself is used for comparison. As with
    groupby, the iterables need to be already sorted according to the key
    function. Duplicates within both iterables will be retained.
    """
    a, b = _keyify(a, key), _keyify(b, key)
    while a and b:
        x, kx = a.peek()
        y, ky = b.peek()
        if kx < ky:
            next(a)
        elif ky < kx:
            next(b)
        else:
            yield x
            next(a)
            next(b)


def difference(a, b, key=None):
    """difference(a, b, key=None) -> all elements in a but not b, in
    sorted order according to key. If the key function is not specified
    or is none, the element itself is used for comparison. As with
    groupby, the iterables need to be already sorted according to the key
    function. Duplicates within the first iterable will be retained.
    """
    a, b = _keyify(a, key), _keyify(b, key)
    while a and b:
        x, kx = a.peek()
        y, ky = b.peek()
        if kx < ky:
            yield x
            next(a)
        elif ky < kx:
            next(b)
        else:
            next(a)
            next(b)
    yield from (x for (x, kx) in a)


def symmetric_difference(a, b, key=None):
    """symmetric_difference(a, b, key=None) -> all elements in either a
    or b, but not both, in sorted order according to key. If the key
    function is not specified or is none, the element itself is used for
    comparison. As with groupby, the iterables need to be already sorted
    according to the key function. Duplicates within either iterable
    will be retained.
    """
    a, b = _keyify(a, key), _keyify(b, key)
    while a and b:
        x, kx = a.peek()
        y, ky = b.peek()
        if kx < ky:
            yield x
            next(a)
        elif ky < kx:
            yield y
            next(b)
        else:
            next(a)
            next(b)
    yield from (x for (x, kx) in a)
    yield from (y for (y, ky) in b)
