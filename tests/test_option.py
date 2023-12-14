"""
test_option.py
Ian Kollipara <ian.kollipara@cune.edu>
2023.12.15

Test Option Monad
"""

# Imports
from monadic_error.option import Some, Nothing


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
def test_some_unwrap():
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
