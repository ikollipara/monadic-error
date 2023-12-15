# Monadic Error
by Ian Kollipara


This is a small library containing 2 monads for handling errors in Python: Attempt (Either) and Option (Maybe).
These two are chosen for their usefulness in handling errors gracefully, and for the ability to slot in nicely with python.
Both monads work with Python 3.10 pattern matching, and as well as MyPy exhaustive pattern matching.

All monads implement `map`, `fmap`, and `unwrap_or`. These all aid in their use in python.
In addition there are a few utility functions for working with the objects during the execution of the program.

## Installation 

To install, run the following command from your terminal:
```
$ pip install monadic-error
```

Or modify your `requirements.txt` with the following line:
```
monadic-error==3.0.0
```

And run
```
$ pip install -r requirements.txt
```

## Attempt

Attempt is the Either monad. The name was chosen to signify how it should be used.
There are two constructors for this: Success and Failure.
Use them as their name denotes.

```python
from monadic_error import Attempt, Success, Failure

def div(x: int, y: int) -> Attempt[ZeroDivisionError, float]:
    if y == 0:
        return Failure(ZeroDivisionError("division by zero"))
    return Success(x / y)

# Or even shorter
from monadic_error import attempt

@attempt
def div(x: int, y: int):
    return x / y
```

## Option

Option is the Maybe Monad. The name was chosen to signify how it should be used.
There are two constructors for this: Some and Nothing.
Use them as their name denotes.

```python
from monadic_error import Option, Some, Nothing

def div(x: int, y: int) -> Option[float]:
    if y == 0:
        return Nothing()
    return Some(x / y)

# Or even shorter

from monadic_error import option

@option
def div(x: int, y: int):
    return x / y
```

## Conversion Between Option and Attempt
There are two utility functions to convert between the two types: `hush` and `note`.

### `hush`
Hush takes an attempt and "hushes" the error, returning an option instead
```python
from monadic_error import hush, Success, Failure

x = Failure(1)
hush(x) # => Nothing()

y = Success(1)
hush(y) # => Some(1)
```

### `note`
Note is the inverse, allowing one to state a reason for the failure, thus turning an option into an attempt.
```python
from monadic_error import note, Some, Nothing

x = Nothing()
note(x, "This is an error") # => Failure("This is an error")

y = Some(1)
note(y, "This is an error") # => Success(1)
```
