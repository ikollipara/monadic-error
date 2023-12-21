"""
attempt.py
Ian Kollipara
2023.01.06

Attempt Monad
"""

# Imports
from abc import ABC, abstractmethod
from typing import Callable, final, TypeGuard

type Attempt[F, S] = Success[F, S] | Failure[F, S]
type Result[S] = Attempt[Exception, S]


class _Attempt[F, S](ABC):
    """Attempt is an Either Monad.

    It encapsulates the ability of something to fail,
    but allows you to note that failure cause.
    In this way, it can be a safer handling of Try-Except Blocks.
    There are a few helper class methods to create from existing
    functions.
    """

    __match_args__ = ("_inner",)

    @abstractmethod
    def __init__(self, inner: F | S) -> None:
        """
        Create an Attempt Monad
        """

    @abstractmethod
    def map[A](self, func: Callable[[S], A]) -> "_Attempt[F, A]":
        """Apply the function to the given Attempt.

        If there is a success value, the function is applied
        and the wrapped back into an Attempt.
        Otherwise, nothing happens.
        """

    @abstractmethod
    def fmap[A](self, func: Callable[[S], "_Attempt[F, A]"]) -> "_Attempt[F, A]":
        """Apply the function to the given attempt.

        If there is a success value, that is used for the function,
        otherwise nothing is done.
        This function allows the composition of two different
        attempt functions.
        """

    @abstractmethod
    def map_f[A](self, func: Callable[[F], A]) -> "_Attempt[A, S]":
        """Same as map, but for the failure track."""

    @abstractmethod
    def fmap_f[A](self, func: Callable[[F], "_Attempt[A, S]"]) -> "_Attempt[A, S]":
        """Same as fmap, but for the failure track."""

    @abstractmethod
    def unwrap_or(self, default: S) -> S:
        """Unwrap the value in success if there is one, otherwise return default."""

    @abstractmethod
    def unwrap_f_or(self, default: F) -> F:
        """Unwrap the value in failure if there is one, otherwise return default."""

    @abstractmethod
    def raise_or(self) -> S:
        """Raise if there is something in the failure, otherwise return success."""

    def is_success(self) -> TypeGuard["Success[F, S]"]: # type: ignore
        """Check if the Attempt is a Success."""
        return isinstance(self, Success)

    def is_failure(self) -> TypeGuard["Failure[F, S]"]: # type: ignore
        """Check if the Attempt is a Failure."""
        return isinstance(self, Failure)


@final
class Success[F, S](_Attempt[F, S]):
    """This represents a successful execution of the program.

    If a raising function does not raise, and returns correctly,
    this is used to signify that.
    """

    def __init__(self, inner: S) -> None:
        self._inner = inner

    def map[A](self, func: Callable[[S], A]) -> Attempt[F, A]:
        return Success(func(self._inner))

    def fmap[A](self, func: Callable[[S], Attempt[F, A]]) -> Attempt[F, A]:
        return func(self._inner)

    def map_f[A](self, _: Callable[[F], A]) -> Attempt[A, S]:
        return Success(self._inner)

    def fmap_f[A](self, _: Callable[[F], Attempt[A, S]]) -> Attempt[A, S]:
        return Success(self._inner)

    def unwrap_or(self, _: S) -> S:
        return self._inner

    def unwrap_f_or(self, default: F) -> F:
        return default

    def raise_or(self) -> S:
        return self._inner

    def __str__(self) -> str:
        return f"<Success _inner={self._inner}>"

    def __eq__(self, __value: Attempt[F, S]) -> bool:
        if isinstance(__value, Success):
            return self._inner == __value._inner
        else:
            return False


@final
class Failure[F, S](_Attempt[F, S]):
    """This represents a failure in the execution of the program.

    If a raising function raises, this should be returned.
    """

    def __init__(self, inner: F) -> None:
        self._inner = inner

    def map[A](self, _: Callable[[S], A]) -> "_Attempt[F, A]":
        return Failure(self._inner)

    def fmap[A](self, _: Callable[[S], "_Attempt[F, A]"]) -> "_Attempt[F, A]":
        return Failure(self._inner)

    def map_f[A](self, func: Callable[[F], A]) -> "_Attempt[A, S]":
        return Failure(func(self._inner))

    def fmap_f[A](self, func: Callable[[F], "_Attempt[A, S]"]) -> "_Attempt[A, S]":
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

    def __eq__(self, __value: Attempt[F, S]) -> bool:
        if isinstance(__value, Failure):
            return self._inner == __value._inner
        else:
            return False
