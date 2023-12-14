"""
test_utils.py
Ian Kollipara <ian.kollipara@cune.edu>
2023.12.14

Test Utility Functions
"""

# Imports
from monadic_error.option import Some, Nothing
from monadic_error.attempt import Success, Failure
from monadic_error.utils import option, from_optional, attempt, note, hush


# Test that a raising function can be attempted
def test_attempt():
    @attempt
    def test_func():
        raise Exception("Test")

    assert isinstance(test_func()._inner, Exception)


# Test that a non-raising function can be attempted
def test_attempt_success():
    @attempt
    def test_func():
        return 1

    assert test_func() == Success(1)


# Test that a raising function can be converted to an option
def test_option():
    @option
    def test_func():
        raise Exception("Test")

    assert test_func() == Nothing()


# Test that a non-raising function can be converted to an option
def test_option_success():
    @option
    def test_func():
        return 1

    assert test_func() == Some(1)


# Test that an optional can be converted to an option
def test_from_optional():
    assert from_optional(1) == Some(1)
    assert from_optional(None) == Nothing()


# Test that an option can be noted
def test_note():
    assert note(Some(1), "Hello") == Success(1)
    assert note(Nothing(), "Hello") == Failure("Hello")


# Test that an attempt can be hushed
def test_hush():
    assert hush(Success(1)) == Some(1)
    assert hush(Failure("Hello")) == Nothing()
