# SPDX-FileCopyrightText: KB Sriram
# SPDX-License-Identifier: MIT

from typing import Any, Callable, Iterator, Optional, Sequence, Tuple, TypeVar, Union
import itertools as it
import pytest
import adafruit_itertools as ait

_K = TypeVar("_K")
_T = TypeVar("_T")


def _take(n: int, iterator: Iterator[_T]) -> Sequence[_T]:
    """Extract the first n elements from a long/infinite iterator."""
    return [v for _, v in zip(range(n), iterator)]


@pytest.mark.parametrize(
    "seq, func",
    [
        ([1, 2, 3, 4], lambda a, x: a - x),
        ([], lambda a, _: a),
        (["abc", "def"], lambda a, x: a + x),
        ("abc", lambda a, x: a + x),
    ],
)
def test_accumulate_with(seq: Sequence[_T], func: Callable[[_T, _T], _T]) -> None:
    x: Sequence[_T] = list(it.accumulate(seq, func))
    y: Sequence[_T] = list(ait.accumulate(seq, func))
    assert x == y


def test_accumulate_types() -> None:
    x_int: Iterator[int] = ait.accumulate([1, 2, 3])
    assert list(x_int) == list(it.accumulate([1, 2, 3]))

    x_bad_type: Iterator[str] = ait.accumulate([1, 2, 3])  # type: ignore[list-item]
    assert list(x_bad_type) == list(it.accumulate([1, 2, 3]))

    x_str_f: Iterator[str] = ait.accumulate("abc", lambda a, x: a + x)
    assert list(x_str_f) == list(it.accumulate("abc", lambda a, x: a + x))

    x_bad_arg_f: Iterator[int] = ait.accumulate(
        [1, 2], lambda a, x: a + ord(x)  # type: ignore[arg-type]
    )
    with pytest.raises(TypeError):
        list(x_bad_arg_f)

    # Note: technically, this works and produces [1, "12"]. But the annotated types
    # are declared to be more strict, and reject accumulator functions that produce
    # mixed types in the result.
    inp = [1, 2]

    def _stringify(acc: Union[int, str], item: int) -> str:
        return str(acc) + str(item)

    x_mixed_f: Iterator[Union[int, str]] = ait.accumulate(inp, _stringify)  # type: ignore[arg-type]
    assert [1, "12"] == list(x_mixed_f)


@pytest.mark.parametrize(
    "arglist, partial",
    [
        ([[1, 2], [3, 4]], 1),
        ([[3]], 1),
        ([[]], 0),
        ([[]], 1),
        ([[], [None]], 1),
        ([[1, "a"], ["b", 2]], 1),
        ([[1, 2, 3], [4, 5, 6]], 4),
    ],
)
def test_chain_basic(arglist: Sequence[Sequence[_T]], partial: int) -> None:
    x: Sequence[_T] = list(ait.chain(*arglist))
    y: Sequence[_T] = list(it.chain(*arglist))
    assert x == y
    xit: Iterator[_T] = ait.chain(*arglist)
    yit: Iterator[_T] = it.chain(*arglist)
    assert _take(partial, xit) == _take(partial, yit)


@pytest.mark.parametrize(
    "arglist, partial",
    [
        ([[1, 2], [3, 4]], 1),
        ([[3]], 1),
        ([[]], 0),
        ([[]], 1),
        ([[], [None]], 1),
        ([[1, "a"], ["b", 2]], 1),
        ([[1, 2, 3], [4, 5, 6]], 4),
    ],
)
def test_chain_from_iterable(arglist: Sequence[Sequence[_T]], partial: int) -> None:
    x: Sequence[_T] = list(ait.chain_from_iterable(arglist))
    y: Sequence[_T] = list(it.chain.from_iterable(arglist))
    assert x == y
    xit: Iterator[_T] = ait.chain_from_iterable(arglist)
    yit: Iterator[_T] = it.chain.from_iterable(arglist)
    assert _take(partial, xit) == _take(partial, yit)


@pytest.mark.parametrize(
    "seq, n",
    [
        ([1, 2, 3, 4], 2),
        ([1, 2, 3, 4], 3),
        ([1, 2, 3], 32),
        ([1, 2, 3], 0),
        ([], 0),
        ([], 1),
    ],
)
def test_combinations(seq: Sequence[_T], n: int) -> None:
    x: Sequence[Tuple[_T, ...]] = list(ait.combinations(seq, n))
    y: Sequence[Tuple[_T, ...]] = list(it.combinations(seq, n))
    assert x == y


@pytest.mark.parametrize(
    "seq, n",
    [
        ([1, 2, 3, 4], 2),
        ([1, 2, 3, 4], 3),
        ([1, 2, 3], 32),
        ([1, 2, 3], 0),
        ([], 0),
        ([], 1),
    ],
)
def test_combo_with_replacement(seq: Sequence[_T], n: int) -> None:
    x: Sequence[Tuple[_T, ...]] = list(ait.combinations_with_replacement(seq, n))
    y: Sequence[Tuple[_T, ...]] = list(it.combinations_with_replacement(seq, n))
    assert x == y


@pytest.mark.parametrize(
    "data, selectors",
    [
        ([1, 2, 3, 4, 5], [True, False, True, False, True]),
        ([1, 2, 3, 4, 5], [True, "", True, True, ""]),
        ([1, 2, 3, 4, 5], [0, 0, None, 0, 0]),
        ([1, 2, 3, 4, 5], [1, 1, 1, True, 1]),
        ([1, 2, 3, 4, 5], [1, 0, 1]),
        ([1, 2, 3, 4, 5], []),
        ([1, 2, 3], [1, 1, 0, 0, 0, 0, 0, 0]),
        ([], [1, 2, 3]),
        ([], []),
    ],
)
def test_compress(data: Sequence[int], selectors: Sequence[Any]) -> None:
    x: Sequence[int] = list(ait.compress(data, selectors))
    y: Sequence[int] = list(it.compress(data, selectors))
    assert x == y


def test_count() -> None:
    assert _take(5, it.count()) == _take(5, ait.count())
    for start in range(-10, 10):
        assert _take(5, it.count(start)) == _take(5, ait.count(start))

    for step in range(-10, 10):
        assert _take(5, it.count(step=step)) == _take(5, ait.count(step=step))

    for start in range(-5, 5):
        for step in range(-5, 5):
            assert _take(10, it.count(start, step)) == _take(10, ait.count(start, step))


@pytest.mark.parametrize(
    "seq",
    [
        ([]),
        ([None]),
        ([1, 2]),
    ],
)
def test_cycle(seq: Sequence[_T]) -> None:
    x: Iterator[_T] = ait.cycle(seq)
    y: Iterator[_T] = it.cycle(seq)
    assert _take(10, x) == _take(10, y)


@pytest.mark.parametrize(
    "predicate, seq",
    [
        (ord, ""),
        (lambda x: x == 42, [1, 2]),
        (lambda x: x == 42, [1, 42]),
    ],
)
def test_dropwhile(predicate: Callable[[_T], object], seq: Sequence[_T]) -> None:
    x: Iterator[_T] = ait.dropwhile(predicate, seq)
    y: Iterator[_T] = it.dropwhile(predicate, seq)
    assert list(x) == list(y)
    bad_type: Iterator[int] = ait.dropwhile(ord, [1, 2])  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        list(bad_type)


@pytest.mark.parametrize(
    "predicate, seq",
    [
        (None, []),
        (None, [1, 0, 2]),
        (lambda x: x % 2, range(10)),
    ],
)
def test_filterfalse(
    predicate: Optional[Callable[[_T], object]], seq: Sequence[_T]
) -> None:
    x: Iterator[_T] = ait.filterfalse(predicate, seq)
    y: Iterator[_T] = it.filterfalse(predicate, seq)
    assert list(x) == list(y)
    bad_type: Iterator[str] = ait.filterfalse(ord, [1, 2])  # type: ignore[list-item]
    with pytest.raises(TypeError):
        list(bad_type)


@pytest.mark.parametrize(
    "data, key",
    [
        ("abcd", ord),
        ("", ord),
        ("aabbcbbbaaa", ord),
        ([(0, 1), (0, 2), (0, 3), (1, 4), (0, 5), (0, 6)], lambda x: x[0]),
        ([(0, 1), (0, 2), (0, 3), (1, 4), (0, 5), (0, 6)], max),
    ],
)
def test_groupby(data: Sequence[_T], key: Callable[[_T], _K]) -> None:
    def _listify(
        iterable: Iterator[Tuple[_K, Iterator[_T]]]
    ) -> Sequence[Tuple[_K, Sequence[_T]]]:
        return [(k, list(group)) for k, group in iterable]

    it_l = _listify(it.groupby(data, key))
    ait_l = _listify(ait.groupby(data, key))
    assert it_l == ait_l


def test_groupby_types() -> None:
    assert list(ait.groupby([])) == list(it.groupby([]))
    assert list(ait.groupby([], key=id)) == list(it.groupby([], key=id))
    assert list(ait.groupby("", ord)) == list(it.groupby("", ord))

    with pytest.raises(TypeError):
        list(ait.groupby("abc", []))  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        list(ait.groupby("abc", chr))  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        ait.groupby(None)  # type: ignore[arg-type]


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


@pytest.mark.parametrize(
    "seq",
    [
        "",
        "A",
        "ABCDEFGH",
    ],
)
def test_permutations(seq: Sequence[_T]) -> None:
    x: Iterator[Tuple[_T, ...]] = ait.permutations(seq)
    y: Iterator[Tuple[_T, ...]] = it.permutations(seq)
    assert list(x) == list(y)

    for r in range(3):
        x = ait.permutations(seq, r)
        y = it.permutations(seq, r)
        assert list(x) == list(y)


@pytest.mark.parametrize(
    "seq",
    [
        "",
        "A",
        "ABCDEFGH",
        [1, 2, "3", None, 4],
    ],
)
def test_product_one(seq: Sequence[object]) -> None:
    x: Iterator[Tuple[object, ...]] = ait.product(seq)
    y: Iterator[Tuple[object, ...]] = it.product(seq)
    assert list(x) == list(y)

    for r in range(3):
        x = ait.product(seq, r=r)
        y = it.product(seq, repeat=r)
        assert list(x) == list(y)


@pytest.mark.parametrize(
    "seq1, seq2",
    [
        ("", []),
        ("", [1, 2]),
        ("AB", []),
        ("ABCDEFGH", [1, 2, 3]),
    ],
)
def test_product_two(seq1: Sequence[str], seq2: Sequence[int]) -> None:
    x: Iterator[Tuple[str, int]] = ait.product(seq1, seq2)
    y: Iterator[Tuple[str, int]] = it.product(seq1, seq2)
    assert list(x) == list(y)

    for r in range(3):
        x_repeat: Iterator[Tuple[object, ...]] = ait.product(seq1, seq2, r=r)
        y_repeat: Iterator[Tuple[object, ...]] = it.product(seq1, seq2, repeat=r)
        assert list(x_repeat) == list(y_repeat)


@pytest.mark.parametrize(
    "element",
    ["", None, 5, "abc"],
)
def test_repeat(element: _T) -> None:
    x: Iterator[_T] = ait.repeat(element)
    y: Iterator[_T] = it.repeat(element)
    assert _take(5, x) == _take(5, y)

    for count in range(10):
        x = ait.repeat(element, count)
        y = it.repeat(element, count)
        assert _take(5, x) == _take(5, y)


@pytest.mark.parametrize(
    "func, seq",
    [
        (pow, [(2, 3), (3, 2), (10, 2)]),
        (lambda x, y: x + y, [("a", "b"), ("c", "d")]),
    ],
)
def test_starmap(func: Callable[[_T, _T], _T], seq: Sequence[Sequence[_T]]) -> None:
    x: Iterator[_T] = ait.starmap(func, seq)
    y: Iterator[_T] = it.starmap(func, seq)
    assert list(x) == list(y)


@pytest.mark.parametrize(
    "func, seq",
    [
        (lambda x: x, []),
        (lambda x: x == 3, [1, 2, 3, 2, 3]),
        (lambda x: x == 3, [1, 2]),
    ],
)
def test_takewhile(func: Callable[[_T], bool], seq: Sequence[_T]) -> None:
    x: Iterator[_T] = ait.takewhile(func, seq)
    y: Iterator[_T] = it.takewhile(func, seq)
    assert list(x) == list(y)


@pytest.mark.parametrize(
    "seq",
    ["", "abc"],
)
def test_tee(seq: Sequence[_T]) -> None:
    x: Sequence[Iterator[_T]] = ait.tee(seq)
    y: Sequence[Iterator[_T]] = it.tee(seq)
    assert [list(v) for v in x] == [list(v) for v in y]

    for n in range(3):
        x = ait.tee(seq, n)
        y = it.tee(seq, n)
        assert [list(v) for v in x] == [list(v) for v in y]


@pytest.mark.parametrize(
    "seq1, seq2",
    [
        ("", []),
        ("", [1, 2]),
        ("abc", []),
        ("abc", [1, 2]),
    ],
)
def test_zip_longest(seq1: Sequence[str], seq2: Sequence[int]) -> None:
    x: Iterator[Tuple[str, int]] = ait.zip_longest(seq1, seq2)
    y: Iterator[Tuple[str, int]] = it.zip_longest(seq1, seq2)
    assert list(x) == list(y)
