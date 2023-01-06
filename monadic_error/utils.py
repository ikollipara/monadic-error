"""
utils.py
Ian Kollipara
2023.01.06

Utility Function
"""

# Imports
from functools import wraps
from typing import Callable, Optional, TypeVar
from .either import Either, Left, Right
from .option import Option, Some, Nothing

A = TypeVar("A")
B = TypeVar("B")

def option(f: Callable[..., A]):
    """ Wrap a raising function and return an Option. """

    @wraps(f)
    def inner(*args, **kwargs) -> Option[A]:
        try:
            return Some(f(*args, **kwargs))
        
        except Exception:
            return Nothing()
    
    return inner

def from_optional(optional: Optional[A]) -> Option[A]:
    """ Convert an Optional to an Option. """

    if optional:
        return Some(optional)
    else:
        return Nothing()

def either(f: Callable[..., A]):
    """ Wrap a raising function and return an Either of Exception and the return type. """

    @wraps(f)
    def inner(*args, **kwargs) -> Either[Exception, A]:
        try:
            return Right(f(*args, **kwargs))
        except Exception as e:
            return Left(e)
    
    return inner

def note(o: Option[A], message: B) -> Either[B, A]:
    """ Convert an Option to Either by adding a note on the left. """

    match o:
        case Some(v):
            return Right(v)
        
        case Nothing():
            return Left(message)

def hush(e: Either[B, A]) -> Option[A]:
    """ Convert an Either to Option by silencing the left. """

    match e:
        case Left(exc):
            return Nothing()
        
        case Right(v):
            return Some(v)