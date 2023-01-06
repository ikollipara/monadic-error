"""
option.py
Ian Kollipara
2023.01.06

Python Option Monad
"""

# Imports
from abc import ABC, abstractmethod
from functools import wraps
from typing import Optional, Self, TypeVar, Generic, Callable

A = TypeVar("A")
R = TypeVar("R")

class Option(ABC, Generic[A]):
    """ Option Monad.

    This is a handler for methods that return Optional.
    This works with current python pattern matching.
    """

    __match_args__ = ("_inner",)

    def __init__(self, inner: A | None) -> None:
        self._inner = inner
    
    @abstractmethod
    def map(self, f: Callable[[A], R]) -> Self[R]:
        """ Apply the function and return a new option. 
        
        f: A -> R
        """

        ...
    
    @abstractmethod
    def fmap(self, f: Callable[[A], Self[R]]) -> Self[R]:
        """ Apply the function and return a new option. 
        
        f: A -> Option[R]
        """
        ...
    
    @abstractmethod
    def lift(self, value: A) -> Self[A]:
        """ Lift a basic value into the Option Scope. """

        ...

class Some(Option[A]):
    def __init__(self, inner: A) -> None:
        self._inner = inner
    
    def map(self, f: Callable[[A], R]) -> Option[R]:
        return Some(f(self._inner))
    
    def fmap(self, f: Callable[[A], Self[R]]) -> Option[R]:
        return f(self._inner)
    
    def lift(self, value: A) -> Self[A]:
        return Some(value)

class Nothing(Option[A]):
    def __init__(self, inner: None = None) -> None:
        self._inner = None
    
    def map(self, f: Callable[[A], R]) -> Option[R]:
        return Nothing()
    
    def fmap(self, f: Callable[[A], Self[R]]) -> Option[R]:
        return Nothing()
    
    def lift(self, value: A) -> Self[A]:
        return Nothing()
