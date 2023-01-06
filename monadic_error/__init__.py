"""
# Monadic Error

This contains two monads implemented to handle errors.
There is also a variety of utility functions to integrate
well with the current ecosystem.
"""

# Exports
from .either import Either, Left, Right
from .option import Option, Some, Nothing
from .utils import hush, note, from_optional, option, either