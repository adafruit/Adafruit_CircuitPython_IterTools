# SPDX-FileCopyrightText: KB Sriram
# SPDX-License-Identifier: MIT

from typing import Iterator, Optional, Sequence, TypeVar
import itertools as it
import pytest
import adafruit_itertools as ait

_T = TypeVar("_T")


@pytest.mark.parametrize(
    "seq, start",
    [
        ("", 0),
        ("", 2),
        ("ABCDEFG", 0),
        ("ABCDEFG", 2),
        ("ABCDEFG", 20),
    ],
)
def test_islice_start(seq: Sequence[_T], start: int) -> None:
    x: Iterator[_T] = ait.islice(seq, start)
    y: Iterator[_T] = it.islice(seq, start)
    assert list(x) == list(y)


@pytest.mark.parametrize(
    "seq, start, stop",
    [
        ("", 0, 5),
        ("", 2, 5),
        ("", 0, 0),
        ("ABCDEFG", 2, 2),
        ("ABCDEFG", 2, 6),
        ("ABCDEFG", 2, None),
        ("ABCDEFG", 2, 17),
        ("ABCDEFG", 20, 30),
    ],
)
def test_islice_start_stop(seq: Sequence[_T], start: int, stop: Optional[int]) -> None:
    x: Iterator[_T] = ait.islice(seq, start, stop)
    y: Iterator[_T] = it.islice(seq, start, stop)
    assert list(x) == list(y)


@pytest.mark.parametrize(
    "seq, start, stop, step",
    [
        ("", 0, 5, 3),
        ("", 2, 5, 2),
        ("", 0, 0, 1),
        ("ABCDEFG", 2, 2, 2),
        ("ABCDEFG", 2, 6, 3),
        ("ABCDEFG", 2, 17, 2),
        ("ABCDEFG", 0, None, 2),
        ("ABCDEFG", 20, 30, 3),
        ("ABCDEFG", 0, None, 3),
    ],
)
def test_islice_start_stop_step(
    seq: Sequence[_T], start: int, stop: Optional[int], step: int
) -> None:
    x: Iterator[_T] = ait.islice(seq, start, stop, step)
    y: Iterator[_T] = it.islice(seq, start, stop, step)
    assert list(x) == list(y)


def test_islice_error() -> None:
    with pytest.raises(ValueError):
        list(ait.islice("abc", -1))
    with pytest.raises(ValueError):
        list(ait.islice("abc", 0, -1))
    with pytest.raises(ValueError):
        list(ait.islice("abc", 0, 0, 0))
