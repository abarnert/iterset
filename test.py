#!/usr/bin/env python3

# TODO: Write proper unit tests.

import iterset


def test_merge():
    a = [5, 10, 15, 20, 25]
    b = [10, 20, 30, 40, 50]
    c = iterset.merge(a, b)
    assert list(c) == [5, 10, 10, 15, 20, 20, 25, 30, 40, 50]


def test_includes():
    a = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
    b = [10, 20, 30, 40]
    assert iterset.includes(a, b)


def test_union():
    a = [5, 10, 15, 20, 25]
    b = [10, 20, 30, 40, 50]
    c = iterset.union(a, b)
    assert list(c) == [5, 10, 15, 20, 25, 30, 40, 50]


def test_intersection():
    a = [5, 10, 15, 20, 25]
    b = [10, 20, 30, 40, 50]
    c = iterset.intersection(a, b)
    assert list(c) == [10, 20]


def test_difference():
    a = [5, 10, 15, 20, 25]
    b = [10, 20, 30, 40, 50]
    c = iterset.difference(a, b)
    assert list(c) == [5, 15, 25]


def test_symmetric_difference():
    a = [5, 10, 15, 20, 25]
    b = [10, 20, 30, 40, 50]
    c = iterset.symmetric_difference(a, b)
    assert list(c) == [5, 15, 25, 30, 40, 50]


if __name__ == "__main__":
    g = globals().copy().items()
    for name, val in g:
        if name.startswith("test_"):
            val()
