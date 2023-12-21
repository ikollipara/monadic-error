"""
option.py
Ian Kollipara
2023.01.06

Python Option Monad
"""

# Imports
from abc import ABC, abstractmethod
from typing import Callable, TypeGuard, final, Generic, overload, Iterable, TypeVar

A = TypeVar("A", covariant=True)

type Option[A] = Some[A] | Nothing[A]


class _Option(ABC, Generic[A]):
    """Option is a Maybe/Option Monad.

    This represents a computation that could fail, but
    you don't care about why it failed.

    The alternative is Attempt (Either Monad) which
    does note why a computation failed.
    """

    __match_args__ = ("_inner",)

    @abstractmethod
    def __init__(self, inner: A | None) -> None:
        """
        Create an Option from a value.
        """

    @abstractmethod
    def map[R](self, func: Callable[[A], R]) -> Option[R]:
        """Apply the function to the given option.

        If something is there, then the function is
        applied, otherwise nothing happens.
        """

    @abstractmethod
    def fmap[R](self, func: Callable[[A], Option[R]]) -> Option[R]:
        """Apply the function to the given option.

        If something is there, then the function is applied,
        otherwise nothing happens.
        This function allows the composition of option functions.
        """

    @abstractmethod
    def unwrap_or(self, default: A) -> A:  # type: ignore
        """Unwrap the value if there is one, otherwise return default."""

    @abstractmethod
    def filter(self, predicate: Callable[[A], bool]) -> Option[A]:
        """Filter the Option based on the predicate."""

    def is_some(self) -> TypeGuard["Some[A]"]: # type: ignore
        """Check if the Option is Some."""
        return isinstance(self, Some)

    def is_nothing(self) -> TypeGuard["Nothing[A]"]: # type: ignore
        """Check if the Option is Nothing."""
        return isinstance(self, Nothing)

    @overload
    @abstractmethod
    def zip[B](self, other: Option[B]) -> Option[tuple[A, B]]:
        """Zip two Options together."""

    @overload
    @abstractmethod
    def zip[*Bs](self, other: Option[Bs]) -> Option[tuple[A, *Bs]]:
        """Zip two Options together."""

    @abstractmethod
    def unwrap(self) -> A:
        """Unwrap the value. Will raise if there is no value."""

    @abstractmethod
    def __eq__(self, __value: "_Option") -> bool:
        """Check if two Options are equal.

        The comparison is based on the inner value.
        """


@final
class Some(_Option[A]):
    """This represents the successful computation.

    If the function returns correctly, then this is shown.
    """

    def __init__(self, inner: A) -> None:
        self._inner = inner

    def map[R](self, func: Callable[[A], R]) -> Option[R]:
        return Some(func(self._inner))

    def fmap[R](self, func: Callable[[A], Option[R]]) -> Option[R]:
        return func(self._inner)

    def unwrap_or(self, _: A) -> A:  # type: ignore
        return self._inner

    def filter(self, predicate: Callable[[A], bool]) -> Option[A]:
        if predicate(self._inner):
            return Some(self._inner)
        else:
            return Nothing()

    def zip[B](self, other: Option[B]) -> Option[tuple[A, B]]:
        if other.is_some():
            if isinstance(other._inner, Iterable):
                return Some((self._inner, *other._inner))  # type: ignore
            return Some((self._inner, other.unwrap()))  # type: ignore
        else:
            return Nothing()

    def unwrap(self) -> A:
        """Unwrap the value."""
        return self._inner

    def __str__(self) -> str:
        return f"<Some _inner={self._inner}>"

    def __eq__(self, __value: Option[A]) -> bool:
        if isinstance(__value, Some):
            return self._inner == __value._inner
        else:
            return False


@final
class Nothing(_Option[A]):
    """This represents the failure of a computation.

    If the function does not return correctly, then this is shown.
    """

    def __init__(self, inner: None = None) -> None:
        self._inner = inner

    def map[R](self, _: Callable[[A], R]) -> Option[R]:
        return Nothing(None)

    def fmap[R](self, _: Callable[[A], Option[R]]) -> Option[R]:
        return Nothing(None)

    def unwrap_or(self, default: A) -> A:  # type: ignore
        return default

    def filter(self, _: Callable[[A], bool]) -> Option[A]:
        return Nothing()

    def zip[B](self, _: Option[B]) -> Option[tuple[A, B]]:
        return Nothing()

    def unwrap(self) -> A:
        """Unwrap the value."""
        raise ValueError("Cannot unwrap Nothing")

    def __str__(self) -> str:
        return "<Nothing>"

    def __eq__(self, __value: Option[A]) -> bool:
        return isinstance(__value, Nothing)
