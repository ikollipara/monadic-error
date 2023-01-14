# Monadic Error
by Ian Kollipara


This is a small library containing 2 monads for handling errors in Python: Attempt (Either) and Option (Maybe).
These two are chosen for their usefulness in handling errors gracefully, and for the ability to slot in nicely with python.
Both monads work with Python 3.10 pattern matching, and as well as MyPy exhaustive pattern matching.

All monads implement `map`, `flatMap`, and `unwrap_or`. These all aid in their use in python.
In addition there are a few utility functions for working with the objects during the execution of the program.

## Attempt

Attempt is the Either monad. The name was chosen to signify how it should be used.
There are two constructors for this: Success and Failure.
Use them as their name denotes.

## Option

Option is the Maybe Monad. The name was chosen to signify how it should be used.
There are two constructors for this: Some and Nothing.
Use them as their name denotes.

