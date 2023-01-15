"""
attempt.py
Ian Kollipara
2023.01.06

Attempt Monad
"""

# Imports
from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Callable, final

F = TypeVar("F")
S = TypeVar("S")
A = TypeVar("A")

class __Attempt(ABC, Generic[F, S]):
    """ Attempt is an Either Monad.
    
    It encapsulates the ability of something to fail,
    but allows you to note that failure cause.
    In this way, it can be a safer handling of Try-Except Blocks.
    There are a few helper class methods to create from existing
    functions.
    """

    __match_args__ = ("_inner",)


    @abstractmethod
    def __init__(self, inner: F | S) -> None:
        self._inner = inner
    
    @abstractmethod
    def map(self, func: Callable[[S], A]) -> "__Attempt[F, A]":
        """Apply the function to the given Attempt.
        
        If there is a success value, the function is applied
        and the wrapped back into an Attempt.
        Otherwise, nothing happens.
        """

        ...
    
    @abstractmethod
    def fmap(self, func: Callable[[S], "__Attempt[F, A]"]) -> "__Attempt[F, A]":
        """Apply the function to the given attempt.

        If there is a success value, that is used for the function,
        otherwise nothing is done.
        This function allows the composition of two different
        attempt functions.
        """

        ...
    
    @abstractmethod
    def map_f(self, func: Callable[[F], A]) -> "__Attempt[A, S]":
        """Same as map, but for the failure track."""

        ...
    
    @abstractmethod
    def fmap_f(self, func: Callable[[F], "__Attempt[A, S]"]) -> "__Attempt[A, S]":
        """Same as fmap, but for the failure track."""

        ...
    
    @abstractmethod
    def unwrap_or(self, default: S) -> S:
        """ Unwrap the value in success if there is one, otherwise return default."""

        ...
    
    @abstractmethod
    def unwrap_f_or(self, default: F) -> F:
        """ Unwrap the value in failure if there is one, otherwise return default."""
        
        ...
    
    @abstractmethod
    def raise_or(self) -> S:
        """ Raise if there is something in the failure, otherwise return success."""

        ...

@final
class Success(__Attempt[F, S]):
    """ This represents a successful execution of the program.
    
    If a raising function does not raise, and returns correctly,
    this is used to signify that.
    """

    def __init__(self, inner: S) -> None:
        self._inner = inner

    def map(self, func: Callable[[S], A]) -> "__Attempt[F, A]":
        return Success(func(self._inner))
    
    def fmap(self, func: Callable[[S], "__Attempt[F, A]"]) -> "__Attempt[F, A]":
        return func(self._inner)
    
    def map_f(self, _: Callable[[F], A]) -> "__Attempt[A, S]":
        return Success(self._inner)
    
    def fmap_f(self, _: Callable[[F], "__Attempt[A, S]"]) -> "__Attempt[A, S]":
        return Success(self._inner)
    
    def unwrap_or(self, _: S) -> S:
        return self._inner
    
    def unwrap_f_or(self, default: F) -> F:
        return default
    
    def raise_or(self) -> S:
        return self._inner
    
    def __str__(self) -> str:
        return f"<Success _inner={self._inner}>"

@final
class Failure(__Attempt[F, S]):
    """ This represents a failure in the execution of the program.
    
    If a raising function raises, this should be returned.
    """

    def __init__(self, inner: F) -> None:
        self._inner = inner
    
    def map(self, _: Callable[[S], A]) -> "__Attempt[F, A]":
        return Failure(self._inner)
    
    def fmap(self, _: Callable[[S], "__Attempt[F, A]"]) -> "__Attempt[F, A]":
        return Failure(self._inner)
    
    def map_f(self, func: Callable[[F], A]) -> "__Attempt[A, S]":
        return Failure(func(self._inner))
    
    def fmap_f(self, func: Callable[[F], "__Attempt[A, S]"]) -> "__Attempt[A, S]":
        return func(self._inner)
    
    def unwrap_or(self, default: S) -> S:
        return default
    
    def unwrap_f_or(self, _: F) -> F:
        return self._inner
    
    def raise_or(self) -> S:
        if isinstance(self._inner, Exception):
            raise self._inner

        raise Exception(self._inner)

    def __str__(self) -> str:
        return f"<Failure _inner={self._inner}>"

Attempt = Success[F, S] | Failure[F, S]

Result = Attempt[Exception, S]
