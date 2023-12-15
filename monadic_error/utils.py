"""
utils.py
Ian Kollipara
2023.01.06

Utility Function
"""

# Imports
from functools import wraps
from typing import Any, Callable, Optional, overload, TypeVar
from .attempt import Attempt, Success, Failure, Result
from .option import Option, Some, Nothing


def option[A](f: Callable[..., A]) -> Callable[..., Option[A]]:
    """Wrap a raising function and return an Option."""

    @wraps(f)
    def inner(*args, **kwargs) -> Option[A]:
        try:
            return Some(f(*args, **kwargs))

        except Exception:
            return Nothing()

    return inner


def from_optional[A](optional: Optional[A]) -> Option[A]:
    """Convert an Optional to an Option."""

    if optional:
        return Some(optional)
    else:
        return Nothing()


def attempt[A](f: Callable[..., A]) -> Callable[..., Result[A]]:
    """Wrap a raising function and return an Attempt of Exception and the return type."""

    @wraps(f)
    def inner(*args, **kwargs) -> Result[A]:
        try:
            return Success(f(*args, **kwargs))
        except Exception as e:
            return Failure(e)

    return inner


@overload
def note[A, B](o: Option[A], message: Callable[..., B]) -> Attempt[B, A]:
    """Convert an Option to Either by adding a note on the left."""


@overload
def note[A, B](o: Option[A], message: B) -> Attempt[B, A]:
    """Convert an Option to Either by adding a note on the left."""


def note[A, B](o: Option[A], message: B | Callable[..., B]) -> Attempt[B, A]:
    """Convert an Option to Either by adding a note on the left."""

    match o:
        case Some(v):
            return Success(v)

        case Nothing():
            if callable(message):
                return Failure(message())
            return Failure(message)


def hush[A](e: Attempt[Any, A]) -> Option[A]:
    """Convert an Either to Option by silencing the left."""

    match e:
        case Failure(_):
            return Nothing()

        case Success(v):
            return Some(v)


A = TypeVar("A", covariant=True)


def flatten(o: Option[Option[A]]) -> Option[A]:
    """Flatten an Option of an Option."""

    match o:
        case Some(v):
            return v

        case _:
            return Nothing()
