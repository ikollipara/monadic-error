"""
test_attempt.py
Ian Kollipara <ian.kollipara@cune.edu>
2023.12.15

Test Attempt Monad
"""

# Imports
from monadic_error.attempt import Success, Failure
from pytest import raises


# Test that Success can be created
def test_success():
    assert Success(1) == Success(1)


# Test that Failure can be created
def test_failure():
    assert Failure(1) == Failure(1)


# Test that Success can be mapped
def test_success_map():
    assert Success(1).map(lambda x: x + 1) == Success(2)


# Test that Failure can be mapped
def test_failure_map():
    assert Failure(1).map(lambda x: x + 1) == Failure(1)


# Test that Success can be fmap'd
def test_success_fmap():
    assert Success(1).fmap(lambda x: Success(x + 1)) == Success(2)


# Test that Failure can be fmap'd
def test_failure_fmap():
    assert Failure(1).fmap(lambda x: Success(x + 1)) == Failure(1)


# Test that Success can be map_f'd
def test_success_map_f():
    assert Success(1).map_f(lambda x: x + 1) == Success(1)


# Test that Failure can be map_f'd
def test_failure_map_f():
    assert Failure(1).map_f(lambda x: x + 1) == Failure(2)


# Test that Success can be fmap_f'd
def test_success_fmap_f():
    assert Success(1).fmap_f(lambda x: Success(x + 1)) == Success(1)


# Test that Failure can be fmap_f'd
def test_failure_fmap_f():
    assert Failure(1).fmap_f(lambda x: Failure(x + 1)) == Failure(2)


# Test that Success can be unwrapped
def test_success_unwrap():
    assert Success(1).unwrap_or(2) == 1


# Test that Failure can be unwrapped
def test_failure_unwrap():
    assert Failure(1).unwrap_or(2) == 2


# Test that Success can be unwrap_f'd
def test_success_unwrap_f():
    assert Success(1).unwrap_f_or(2) == 2


# Test that Failure can be unwrap_f'd
def test_failure_unwrap_f():
    assert Failure(1).unwrap_f_or(2) == 1


# Test that Failure can be raised
def test_failure_raise():
    with raises(Exception):
        Failure(Exception()).raise_or()


# Test that Failure can be raised with a non-Exception value
def test_failure_raise_non_exception():
    with raises(Exception):
        Failure(1).raise_or()


# Test that Success can be raised
def test_success_raise():
    assert Success(1).raise_or() == 1


# Test that Success can equal Success
def test_success_eq_success():
    assert Success(1) == Success(1)


# Test that Success cannot equal Failure
def test_success_neq_failure():
    assert Success(1) != Failure(1)


# Test that Failure can equal Failure
def test_failure_eq_failure():
    assert Failure(1) == Failure(1)


# Test that Failure cannot equal Success
def test_failure_neq_success():
    assert Failure(1) != Success(1)


# Test Success String
def test_success_str():
    assert str(Success(1)) == "<Success _inner=1>"


# Test Failure String
def test_failure_str():
    assert str(Failure(1)) == "<Failure _inner=1>"
