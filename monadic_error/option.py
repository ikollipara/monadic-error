"""
option.py
Ian Kollipara
2023.01.06

Python Option Monad
"""

# Imports
from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Callable

A = TypeVar("A")
R = TypeVar("R")

class __Option(ABC, Generic[A]):
    """ Option is a Maybe/Option Monad.
    
    This represents a computation that could fail, but
    you don't care about why it failed.

    The alternative is Attempt (Either Monad) which
    does note why a computation failed.
    """

    __match_args__ = ("_inner",)

    @abstractmethod
    def __init__(self, inner: A | None) -> None:
        self._inner = inner
    
    @abstractmethod
    def map(self, func: Callable[[A], R]) -> "__Option[R]":
        """ Apply the function to the given option.
        
        If something is there, then the function is
        applied, otherwise nothing happens.
        """

        ...
    
    @abstractmethod
    def fmap(self, func: Callable[[A], "__Option[R]"]) -> "__Option[R]":
        """ Apply the function to the given option.
        
        If something is there, then the function is applied,
        otherwise nothing happens.
        This function allows the composition of option functions.
        """

        ...
    
    @abstractmethod
    def unwrap_or(self, default: A) -> A:
        """ Unwrap the value if there is one, otherwise return default."""

        ...
    

class Some(__Option[A]):
    """ This represents the successful computation.
    
    If the function returns correctly, then this is shown.
    """

    def __init__(self, inner: A) -> None:
        self._inner = inner
    
    def map(self, func: Callable[[A], R]) -> "__Option[R]":
        return Some(func(self._inner))
    
    def fmap(self, func: Callable[[A], "__Option[R]"]) -> "__Option[R]":
        return func(self._inner)
    
    def unwrap_or(self, _: A) -> A:
        return self._inner
    
    def __str__(self) -> str:
        return f"<Some _inner={self._inner}>"
    
    

class Nothing(__Option[A]):
    """ This represents the failure of a computation.
    
    If the function does not return correctly, then this is shown.
    """

    def __init__(self, inner: None = None) -> None:
        self._inner = inner

    def map(self, _: Callable[[A], R]) -> "__Option[R]":
        return Nothing(None)
    
    def fmap(self, _: Callable[[A], "__Option[R]"]) -> "__Option[R]":
        return Nothing(None)
    
    def unwrap_or(self, default: A) -> A:
        return default
    
    def __str__(self) -> str:
        return "<Nothing>"
    

Option = Some[A] | Nothing[A]