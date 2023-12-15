"""
# Monadic Error

This contains two monads implemented to handle errors.
There is also a variety of utility functions to integrate
well with the current ecosystem.
"""

# Exports
from .attempt import Attempt, Success, Failure
from .option import Option, Some, Nothing
from .utils import attempt, option, from_optional, note, hush, flatten
