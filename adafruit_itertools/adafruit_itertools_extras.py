# 1. This LICENSE AGREEMENT is between the Python Software Foundation ("PSF"), and
#    the Individual or Organization ("Licensee") accessing and otherwise using Python
#    3.7.3 software in source or binary form and its associated documentation.

# 2. Subject to the terms and conditions of this License Agreement, PSF hereby
#    grants Licensee a nonexclusive, royalty-free, world-wide license to reproduce,
#    analyze, test, perform and/or display publicly, prepare derivative works,
#    distribute, and otherwise use Python 3.7.3 alone or in any derivative
#    version, provided, however, that PSF's License Agreement and PSF's notice of
#    copyright, i.e., "Copyright © 2001-2019 Python Software Foundation; All Rights
#    Reserved" are retained in Python 3.7.3 alone or in any derivative version
#    prepared by Licensee.

# 3. In the event Licensee prepares a derivative work that is based on or
#    incorporates Python 3.7.3 or any part thereof, and wants to make the
#    derivative work available to others as provided herein, then Licensee hereby
#    agrees to include in any such work a brief summary of the changes made to Python
#    3.7.3.

# 4. PSF is making Python 3.7.3 available to Licensee on an "AS IS" basis.
#    PSF MAKES NO REPRESENTATIONS OR WARRANTIES, EXPRESS OR IMPLIED.  BY WAY OF
#    EXAMPLE, BUT NOT LIMITATION, PSF MAKES NO AND DISCLAIMS ANY REPRESENTATION OR
#    WARRANTY OF MERCHANTABILITY OR FITNESS FOR ANY PARTICULAR PURPOSE OR THAT THE
#    USE OF PYTHON 3.7.3 WILL NOT INFRINGE ANY THIRD PARTY RIGHTS.

# 5. PSF SHALL NOT BE LIABLE TO LICENSEE OR ANY OTHER USERS OF PYTHON 3.7.3
#    FOR ANY INCIDENTAL, SPECIAL, OR CONSEQUENTIAL DAMAGES OR LOSS AS A RESULT OF
#    MODIFYING, DISTRIBUTING, OR OTHERWISE USING PYTHON 3.7.3, OR ANY DERIVATIVE
#    THEREOF, EVEN IF ADVISED OF THE POSSIBILITY THEREOF.

# 6. This License Agreement will automatically terminate upon a material breach of
#    its terms and conditions.

# 7. Nothing in this License Agreement shall be deemed to create any relationship
#    of agency, partnership, or joint venture between PSF and Licensee.  This License
#    Agreement does not grant permission to use PSF trademarks or trade name in a
#    trademark sense to endorse or promote products or services of Licensee, or any
#    third party.

# 8. By copying, installing or otherwise using Python 3.7.3, Licensee agrees
#    to be bound by the terms and conditions of this License Agreement.
"""
`adafruit_itertools_extras`
================================================================================

Extras for Python itertools adapted for CircuitPython by Dave Astels

This module contains an extended toolset using the existing itertools as
building blocks.

The extended tools offer the same performance as the underlying
toolset. The superior memory performance is kept by processing elements one at
a time rather than bringing the whole iterable into memory all at once. Code
volume is kept small by linking the tools together in a functional style which
helps eliminate temporary variables. High speed is retained by preferring
"vectorized" building blocks over the use of for-loops and generators which
incur interpreter overhead.

Copyright 2001-2019 Python Software Foundation; All Rights Reserved

* Author(s): The PSF and Dave Astels

Implementation Notes
--------------------

Based on code from the offical Python documentation.

**Hardware:**

**Software and Dependencies:**

* Adafruit's CircuitPython port of itertools
* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases
"""

#pylint:disable=invalid-name,deprecated-lambda,keyword-arg-before-vararg

import adafruit_itertools as it

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_Itertools.git"


def all_equal(iterable):
    """Returns True if all the elements are equal to each other.

    :param iterable: source of values

    """
    g = it.groupby(iterable)
    next(g)                               # should succeed, value isn't relevant
    try:
        next(g)                           # should fail: only 1 group
        return False
    except StopIteration:
        return True


def dotproduct(vec1, vec2):
    """Compute the dot product of two vectors.

    :param vec1: the first vector
    :param vec2: the second vector

    """
    # dotproduct([1, 2, 3], [1, 2, 3]) -> 14
    return sum(map(lambda x, y: x * y, vec1, vec2))


def first_true(iterable, default=False, pred=None):
    """Returns the first true value in the iterable.

    If no true value is found, returns *default*

    If *pred* is not None, returns the first item for which pred(item)
    is true.

    :param iterable: source of values
    :param default: the value to return if no true value is found (default is
                    False)
    :param pred: if not None test the result of applying pred to each value
                 instead of the values themselves (default is None)

    """
    # first_true([a,b,c], x) --> a or b or c or x
    # first_true([a,b], x, f) --> a if f(a) else b if f(b) else x
    try:
        return next(filter(pred, iterable))
    except StopIteration:
        return default


def flatten(iterable_of_iterables):
    """Flatten one level of nesting.

    :param iterable_of_iterables: a sequence of iterables to flatten

    """
    # flatten(['ABC', 'DEF']) --> A B C D E F
    return it.chain_from_iterable(iterable_of_iterables)


def grouper(iterable, n, fillvalue=None):
    """Collect data into fixed-length chunks or blocks.

    :param iterable: source of values
    :param n: chunk size
    :param fillvalue: value to use for filling out the final chunk.
                      Defaults to None.

    """
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return it.zip_longest(*args, fillvalue=fillvalue)


def iter_except(func, exception):
    """ Call a function repeatedly, yielding the results, until exception is raised.

    Converts a call-until-exception interface to an iterator interface.
    Like builtins.iter(func, sentinel) but uses an exception instead
    of a sentinel to end the loop.

    Examples:
        iter_except(functools.partial(heappop, h), IndexError)   # priority queue iterator
        iter_except(d.popitem, KeyError)                         # non-blocking dict iterator
        iter_except(d.popleft, IndexError)                       # non-blocking deque iterator
        iter_except(q.get_nowait, Queue.Empty)                   # loop over a producer Queue
        iter_except(s.pop, KeyError)                             # non-blocking set iterator

    :param func: the function to call repeatedly
    :param exception: the exception upon which to stop

    """
    try:
        while True:
            yield func()
    except exception:
        pass


def ncycles(iterable, n):
    """Returns the sequence elements a number of times.

    :param iterable: the source of values
    :param n: how many time to repeal the values

    """
    return it.chain_from_iterable(it.repeat(tuple(iterable), n))


def nth(iterable, n, default=None):
    """Returns the nth item or a default value.

    :param iterable: the source of values
    :param n: the index of the item to fetch, starts at 0

    """
    try:
        return next(it.islice(iterable, n, n+1))
    except StopIteration:
        return default

def padnone(iterable):
    """Returns the sequence elements and then returns None indefinitely.

    Useful for emulating the behavior of the built-in map() function.

    :param iterable: the source of initial values
    """
    # take(5, padnone([1, 2, 3])) -> 1 2 3 None None
    return it.chain(iterable, it.repeat(None))


def pairwise(iterable):
    """Pair up valuesin the iterable.

    :param iterable: source of values

    """
    # pairwise(range(11)) -> (1, 2), (3, 4), (5, 6), (7, 8), (9, 10)
    a, b = it.tee(iterable)
    try:
        next(b)
    except StopIteration:
        pass
    return zip(a, b)


def partition(pred, iterable):
    """Use a predicate to partition entries into false entries and true entries.

    :param pred: the predicate that divides the values
    :param iterable: source of values

    """
    # partition(lambda x: x % 2, range(10)) --> 0 2 4 6 8   and  1 3 5 7 9
    t1, t2 = it.tee(iterable)
    return it.filterfalse(pred, t1), filter(pred, t2)


def prepend(value, iterator):
    """Prepend a single value in front of an iterator

    :param value: the value to prepend
    :param iterator: the iterator to which to prepend

    """
    # prepend(1, [2, 3, 4]) -> 1 2 3 4
    return it.chain([value], iterator)


def quantify(iterable, pred=bool):
    """Count how many times the predicate is true.

    :param iterable: source of values
    :param pred: the predicate whose result is to be quantified when applied to
                 all values in iterable. Defaults to bool()

    """
    # quantify([2, 56, 3, 10, 85], lambda x: x >= 10) -> 3
    return sum(map(pred, iterable))


def repeatfunc(func, times=None, *args):
    """Repeat calls to func with specified arguments.

    Example:  repeatfunc(random.random)

    :param func: the function to be called
    :param times: the number of times to call it: size of the resulting iterable
                  None means infinitely. Default is None.

    """
    if times is None:
        return it.starmap(func, it.repeat(args))
    return it.starmap(func, it.repeat(args, times))


def roundrobin(*iterables):
    """Return an iterable created by repeatedly picking value from each
    argument in order.

    :param args: the iterables to pick from

    """
    # roundrobin('ABC', 'D', 'EF') --> A D E B F C
    # Recipe credited to George Sakkis
    num_active = len(iterables)
    nexts = it.cycle(iter(it).__next__ for it in iterables)
    while num_active:
        try:
            for n in nexts:
                yield n()
        except StopIteration:
            # Remove the iterator we just exhausted from the cycle.
            num_active -= 1
            nexts = it.cycle(it.islice(nexts, num_active))


def tabulate(function, start=0):
    """Apply a function to a sequence of consecutive integers.

    :param function: the function of one integer argument
    :param start: optional value to start at (default is 0)

    """
    # take(5, tabulate(lambda x: x * x))) -> 0 1 4 9 16
    return map(function, it.count(start))


def tail(n, iterable):
    """Return an iterator over the last n items

    :param n: how many values to return
    :param iterable: the source of values

    """
    # tail(3, 'ABCDEFG') --> E F G
    i = iter(iterable)
    buf = []
    while True:
        try:
            buf.append(next(i))
            if len(buf) > n:
                buf.pop(0)
        except StopIteration:
            break
    return iter(buf)


def take(n, iterable):
    """Return first n items of the iterable as a list

    :param n: how many values to take
    :param iterable: the source of values

    """
    # take(3, 'ABCDEF')) -> A B C
    return list(it.islice(iterable, n))
