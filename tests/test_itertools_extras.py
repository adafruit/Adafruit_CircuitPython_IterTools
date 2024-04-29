# SPDX-FileCopyrightText: KB Sriram
# SPDX-License-Identifier: MIT

from typing import (
    Callable,
    Iterator,
    Optional,
    Sequence,
    TypeVar,
)
from typing_extensions import TypeAlias

import more_itertools as itextras
import pytest
from adafruit_itertools import adafruit_itertools_extras as aextras

_K = TypeVar("_K")
_T = TypeVar("_T")
_S = TypeVar("_S")
_Predicate: TypeAlias = Callable[[_T], bool]


def _take(n: int, iterator: Iterator[_T]) -> Sequence[_T]:
    """Extract the first n elements from a long/infinite iterator."""
    return [v for _, v in zip(range(n), iterator)]


@pytest.mark.parametrize(
    "data",
    [
        "aaaa",
        "abcd",
        "a",
        "",
        (1, 2),
        (3, 3),
        ("", False),
        (42, True),
    ],
)
def test_all_equal(data: Sequence[_T]) -> None:
    assert itextras.all_equal(data) == aextras.all_equal(data)


@pytest.mark.parametrize(
    ("vec1", "vec2"),
    [
        ([1, 2], [3, 4]),
        ([], []),
        ([1], [2, 3]),
        ([4, 5], [6]),
    ],
)
def test_dotproduct(vec1: Sequence[int], vec2: Sequence[int]) -> None:
    assert itextras.dotproduct(vec1, vec2) == aextras.dotproduct(vec1, vec2)


@pytest.mark.parametrize(
    ("seq", "dflt", "pred"),
    [
        ([0, 2], 0, None),
        ([], 10, None),
        ([False], True, None),
        ([1, 2], -1, lambda _: False),
        ([0, 1], -1, lambda _: True),
        ([], -1, lambda _: True),
    ],
)
def test_first_true(
    seq: Sequence[_T], dflt: _T, pred: Optional[_Predicate[_T]]
) -> None:
    assert itextras.first_true(seq, dflt, pred) == aextras.first_true(seq, dflt, pred)


@pytest.mark.parametrize(
    ("seq1", "seq2"),
    [
        ("abc", "def"),
        ("", "def"),
        ("abc", ""),
        ("", ""),
    ],
)
def test_flatten(seq1: str, seq2: str) -> None:
    assert list(itextras.flatten(seq1 + seq2)) == list(aextras.flatten(seq1 + seq2))
    for repeat in range(3):
        assert list(itextras.flatten([seq1] * repeat)) == list(
            aextras.flatten([seq1] * repeat)
        )
        assert list(itextras.flatten([seq2] * repeat)) == list(
            aextras.flatten([seq2] * repeat)
        )


@pytest.mark.parametrize(
    ("seq", "count", "fill"),
    [
        ("abc", 3, None),
        ("abcd", 3, None),
        ("abc", 3, "x"),
        ("abcd", 3, "x"),
        ("abc", 0, None),
        ("", 3, "xy"),
    ],
)
def test_grouper(seq: Sequence[str], count: int, fill: Optional[str]) -> None:
    assert list(itextras.grouper(seq, count, fillvalue=fill)) == list(
        aextras.grouper(seq, count, fillvalue=fill)
    )


@pytest.mark.parametrize(
    ("data"),
    [
        (1, 2, 3),
        (),
    ],
)
def test_iter_except(data: Sequence[int]) -> None:
    assert list(itextras.iter_except(list(data).pop, IndexError)) == list(
        aextras.iter_except(list(data).pop, IndexError)
    )


@pytest.mark.parametrize(
    ("seq", "count"),
    [
        ("abc", 4),
        ("abc", 0),
        ("", 4),
    ],
)
def test_ncycles(seq: str, count: int) -> None:
    assert list(itextras.ncycles(seq, count)) == list(aextras.ncycles(seq, count))


@pytest.mark.parametrize(
    ("seq", "n", "dflt"),
    [
        ("abc", 1, None),
        ("abc", 10, None),
        ("abc", 10, "x"),
        ("", 0, None),
    ],
)
def test_nth(seq: str, n: int, dflt: Optional[str]) -> None:
    assert itextras.nth(seq, n, dflt) == aextras.nth(seq, n, dflt)


@pytest.mark.parametrize(
    ("seq"),
    [
        "abc",
        "",
    ],
)
def test_padnone(seq: str) -> None:
    assert _take(10, itextras.padnone(seq)) == _take(10, aextras.padnone(seq))


@pytest.mark.parametrize(
    ("seq"),
    [
        (),
        (1,),
        (1, 2),
        (1, 2, 3),
        (1, 2, 3, 4),
    ],
)
def test_pairwise(seq: Sequence[int]) -> None:
    assert list(itextras.pairwise(seq)) == list(aextras.pairwise(seq))


@pytest.mark.parametrize(
    ("pred", "seq"),
    [
        (lambda x: x % 2, (0, 1, 2, 3)),
        (lambda x: x % 2, (0, 2)),
        (lambda x: x % 2, ()),
    ],
)
def test_partition(pred: _Predicate[int], seq: Sequence[int]) -> None:
    # assert list(itextras.partition(pred, seq)) == list(aextras.partition(pred, seq))
    true1, false1 = itextras.partition(pred, seq)
    true2, false2 = aextras.partition(pred, seq)
    assert list(true1) == list(true2)
    assert list(false1) == list(false2)


@pytest.mark.parametrize(
    ("value", "seq"),
    [
        (1, (2, 3)),
        (1, ()),
    ],
)
def test_prepend(value: int, seq: Sequence[int]) -> None:
    assert list(itextras.prepend(value, seq)) == list(aextras.prepend(value, seq))


@pytest.mark.parametrize(
    ("seq", "pred"),
    [
        ((0, 1), lambda x: x % 2 == 0),
        ((1, 1), lambda x: x % 2 == 0),
        ((), lambda x: x % 2 == 0),
    ],
)
def test_quantify(seq: Sequence[int], pred: _Predicate[int]) -> None:
    assert itextras.quantify(seq) == aextras.quantify(seq)
    assert itextras.quantify(seq, pred) == aextras.quantify(seq, pred)


@pytest.mark.parametrize(
    ("func", "times", "args"),
    [
        (lambda: 1, 5, []),
        (lambda: 1, 0, []),
        (lambda x: x + 1, 10, [3]),
        (lambda x, y: x + y, 10, [3, 4]),
    ],
)
def test_repeatfunc(func: Callable, times: int, args: Sequence[int]) -> None:
    assert _take(5, itextras.repeatfunc(func, None, *args)) == _take(
        5, aextras.repeatfunc(func, None, *args)
    )
    assert list(itextras.repeatfunc(func, times, *args)) == list(
        aextras.repeatfunc(func, times, *args)
    )


@pytest.mark.parametrize(
    ("seq1", "seq2"),
    [
        ("abc", "def"),
        ("a", "bc"),
        ("ab", "c"),
        ("", "abc"),
        ("", ""),
    ],
)
def test_roundrobin(seq1: str, seq2: str) -> None:
    assert list(itextras.roundrobin(seq1)) == list(aextras.roundrobin(seq1))
    assert list(itextras.roundrobin(seq1, seq2)) == list(aextras.roundrobin(seq1, seq2))


@pytest.mark.parametrize(
    ("func", "start"),
    [
        (lambda x: 2 * x, 17),
        (lambda x: -x, -3),
    ],
)
def test_tabulate(func: Callable[[int], int], start: int) -> None:
    assert _take(5, itextras.tabulate(func)) == _take(5, aextras.tabulate(func))
    assert _take(5, itextras.tabulate(func, start)) == _take(
        5, aextras.tabulate(func, start)
    )


@pytest.mark.parametrize(
    ("n", "seq"),
    [
        (3, "abcdefg"),
        (0, "abcdefg"),
        (10, "abcdefg"),
        (5, ""),
    ],
)
def test_tail(n: int, seq: str) -> None:
    assert list(itextras.tail(n, seq)) == list(aextras.tail(n, seq))


@pytest.mark.parametrize(
    ("n", "seq"),
    [
        (3, "abcdefg"),
        (0, "abcdefg"),
        (10, "abcdefg"),
        (5, ""),
    ],
)
def test_take(n: int, seq: str) -> None:
    assert list(itextras.take(n, seq)) == list(aextras.take(n, seq))
