"""
test_option.py
Ian Kollipara <ian.kollipara@cune.edu>
2023.12.15

Test Option Monad
"""

# Imports
from monadic_error.option import Some, Nothing
from pytest import raises


# Test that Some can be created
def test_some():
    assert Some(1) == Some(1)


# Test that Nothing can be created
def test_nothing():
    assert Nothing() == Nothing()


# Test that Some can be mapped
def test_some_map():
    assert Some(1).map(lambda x: x + 1) == Some(2)


# Test that Nothing can be mapped
def test_nothing_map():
    assert Nothing().map(lambda x: x + 1) == Nothing()


# Test that Some can be fmap'd
def test_some_fmap():
    assert Some(1).fmap(lambda x: Some(x + 1)) == Some(2)


# Test that Nothing can be fmap'd
def test_nothing_fmap():
    assert Nothing().fmap(lambda x: Some(x + 1)) == Nothing()


# Test that Some can be unwrapped
def test_some_unwrap_or_1():
    assert Some(1).unwrap_or(2) == 1


# Test that Nothing can be unwrapped
def test_nothing_unwrap():
    assert Nothing().unwrap_or(2) == 2


# Test that Some can equal Some
def test_some_eq_some():
    assert Some(1) != Some(2)


# Test that Some cannot equal Nothing
def test_some_neq_nothing():
    assert Some(1) != Nothing()


# Test Nothing String
def test_nothing_str():
    assert str(Nothing()) == "<Nothing>"


# Test Some String
def test_some_str():
    assert str(Some(1)) == "<Some _inner=1>"


# Test that Some can be filtered
def test_some_filter():
    assert Some(1).filter(lambda x: x == 1) == Some(1)


# Test that Some is_some
def test_some_is_some():
    assert Some(1).is_some()


# Test that Nothing is not_some
def test_nothing_is_not_some():
    assert not Nothing().is_some()


# Test that Some is not nothing
def test_some_is_not_nothing():
    assert not Some(1).is_nothing()


# Test that Nothing is nothing
def test_nothing_is_nothing():
    assert Nothing().is_nothing()


# Test that Nothing filter is nothing
def test_nothing_filter():
    assert Nothing().filter(lambda x: x == 1) == Nothing()


# Test that Some not passing filter is nothing
def test_some_filter_not_passing():
    assert Some(1).filter(lambda x: x == 2) == Nothing()


# Test that Some unwraps correctly
def test_some_unwrap():
    assert Some(1).unwrap() == 1


# Test that Nothing unwrapped raises
def test_nothing_unwrap_raises():
    with raises(ValueError):
        Nothing().unwrap()


# Test that Some unwrap_or returns correct value
def test_some_unwrap_or():
    assert Some(1).unwrap_or(2) == 1


# Test that Nothing unwrap_or returns default value
def test_nothing_unwrap_or():
    assert Nothing().unwrap_or(2) == 2


# Test that Some can be zipped
def test_some_zip():
    assert Some(1).zip(Some(2)) == Some((1, 2))  # type: ignore


# Test that Some zipped with a Some with a tuple returns a tuple
def test_some_zip_tuple():
    assert Some(1).zip(Some((2, 3))) == Some((1, 2, 3))  # type: ignore


# Test that Some zipped with Nothing returns Nothing
def test_some_zip_nothing():
    assert Some(1).zip(Nothing()) == Nothing()  # type: ignore


# Test that Nothing zipped with Some returns Nothing
def test_nothing_zip_some():
    assert Nothing().zip(Some(1)) == Nothing()  # type: ignore
