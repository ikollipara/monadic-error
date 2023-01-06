"""
either.py
Ian Kollipara
2023.01.06

Either Monad
"""

# Imports
from abc import ABC, abstractmethod
from functools import wraps
from typing import Self, TypeVar, Generic, Callable

L = TypeVar("L")
R = TypeVar("R")
A = TypeVar("A")

class Either(ABC, Generic[L, R]):
    """ Either Monad.

    This is for functions that could fail and
    you want to track that failure.
    """

    __match_args__ = ("_inner",)

    @abstractmethod
    def __init__(self, inner: L | R) -> None:
        self._inner = inner
    
    @abstractmethod
    def map(self, f: Callable[[R], A]) -> Self[L, A]:
        """ Map against the right side.
        
        f: R -> A
        """
        ...
    
    @abstractmethod
    def left_map(self, f: Callable[[L], A]) -> Self[A, R]:
        """ Map against the left side.
        
        f: L -> A
        """

        ...
    
    @abstractmethod
    def lift(self, value: A) -> Self[L, A]:
        """ Lift a value into the exception context. """

        ...

    
    @abstractmethod
    def fmap(self, f: Callable[[R], Self[L, A]]) -> Self[L, A]:
        ...
    
    @abstractmethod
    def left_fmap(self, f: Callable[[L], Self[A, R]]) -> Self[A, R]:
        ...
    
class Left(Either[L, R]):

    def __init__(self, inner: L) -> None:
        self._inner = inner
    
    def map(self, f):
        return Left(self._inner)
    
    def left_map(self, f):
        return Left(f(self._inner))
    
    def fmap(self, f):
        return Left(self._inner)
    
    def left_fmap(self, f):
        return f(self._inner)
    
    def lift(self, value: A) -> Self[L, A]:
        return Left(None)

class Right(Either[L, R]):

    def __init__(self, inner: R) -> None:
        self._inner = inner
    
    def map(self, f):
        return Right(f(self._inner))
    
    def left_map(self, f):
        return Right(self._inner)
    
    def fmap(self, f):
        return f(self._inner)
    
    def left_fmap(self, f):
        return Right(self._inner)
    
    def lift(self, value: A) -> Self[L, A]:
        return Right(value)
