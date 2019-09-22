# iterset
Set operations on sorted iterables

This module implements set operations on sorted iterables.

Each function takes a pair of iterables and an optional key
function. As with `itertools.groupby`, the iterables should be sorted
by that key. The output will be sorted by the same key.

## Functions

In general, the results should be identical to the equivalent C++
standard library functions from `<algorithms>`.

 * `merge`: equivalent to C++ `merge`
 * `includes`: equivalent to C++ `includes`
 * `union`: equivalent to C++ `set_union`
 * `intersection`: equivalent to C++ `set_intersection`
 * `difference`: equivalent to C++ `set_difference`
 * `symmetric_difference`: equivalent to C++
   `set_symmetric_difference`
   
In addition, for consistency of the `set` type:

 * `issuperset`: same as `includes`
 * `issubset`: same as `includes` with the arguments reversed

While `union` and `merge` might seem redundant, they're not the same
operation. For example, the union of `[1, 2, 3]` and `[2, 4, 6]` is
`[1, 2, 3, 4, 6]`, because `2` appears one time in at least one
input. But the merge is `[1, 2, 2, 3, 4, 6]`, because `2` appears one
time in the first input plus one time in the second.

## Comparison to sets

In most cases, the same operations could be done more simply by just
putting one or both iterables in `set`s (or, if they represent
multisets, `collection.Counter`s). For example, assuming `a` and `b`
are sorted and contain no duplicates, these will both give you an
iterable with all elements in either `a` or `b`:

    iterset.intersection(a, b)
	set(a).intersection(b)

There are usually performance advantages to using `set`, but they're
both linear operations, and there are some cases where `iterset` might
be faster (e.g., a very large `list` of strings allocated in sorted
order in a fresh process will probably have very good cache locality
at all three levels, while a `set` will not).

However, there are usually other differences that matter more:

 * `iterset` does not require hashable (or immutable) values.
 * `iterset` requires sorted inputs.
 * `iterset` preserves sort order.
 * `iterset` allows arbitrary key functions rather than matching on
             the values themselves.
 * `iterset` requires a total ordering (on the keys).
 * `iterset` allows both inputs to be lazy; with `set`, at least one
             has to be read into memory and stored in a `set`.
 * `iterset` logic for duplicates is not identical to either `set` or
             `Counter`, and in some cases is the logic you want.
 * `iterset` has `merge`, which doesn't make sense for `set`.
 * `iterset` doesn't look as nice as operators on the sets themselves
             when doing lots of set algebra.

## Implementation 

The algorithms all work by step-comparison: compare the current
values, then step forward on one or the other or both, until they're
exhausted.

The algorithms should match the definitions of the corresponding C++
functions. (Possibly not the implementations in any specific C++
standard library implementation, as they presumably have some
optimizations--e.g., the most obvious way to check and fall back to
`yield from` / `std::copy` is not always the fastest.)

## Version

 * 0.0.1: 2019-09-22: First working version.
 
# TODO

 * More complete unit test suite. See Python's tests for `set`, and
   (if license allows) `libc++` or another implementation for the C++
   functions.

 * Extend to more than 2 iterables (and the trivial 1- and 0-iterable
   cases)? Check what the `set` methods do, but I think they handle
   this (except for 0, of course).

 * `inplace_merge`? While this is useful, it doesn't fit the model of
   the other operations. (In C++, it works on any bidirectional
   writable iterators, but there is no such thing in Python.)
   
 * `partition`? Tends to be useful with `merge`, but it's already in
   the `itertools` docs recipes, and `more-itertools` and `toolz`, so
   is it needed here as well?

 * To simplify the implementation, each iterable is converted to a
   peekable iterator of (value, key) pairs. This almost certainly has
   some performance impact. Once a more complete unit test suite is
   available, it's probably worth making them work directly on `next`
   and local variables and benchmarking.

 * See if a C implementation helps performance. (This would be
   necessary if these functions are to be added to `itertools`, unless
   `itertools` is split into Python plus C modules, which has been
   suggested many times but nobody's actually done it.)

 * There are some other obvious optimizations. For example, if we
   exhaust `a` during `union`, instead of yielding from the first of
   each (value, key) pair in the key-ified `b` iterator (which calls
   the key function only to throw the result away, and also stacks up
   an extra generator that each element has to go through), we could
   just yield from `b` itself.

 * See if `more-itertools` has any useful helpers--I think it has a
   fully-tested `peekaable`. (This would be a good idea if these
   functions are to be added to `more-itertools`.)
 
 * `setuptools`-ify, docs, and PyPI.
