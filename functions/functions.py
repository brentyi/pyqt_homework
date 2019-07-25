#!/usr/bin/python3

import abc
import numpy as np


class FunctionBase(abc.ABC):
    """Abstract base class for arbitrary 2-parameter functions.

    Args:
        a (float): Initial value for attribute a. Defaults to 0.
        b (float): Initial value for attribute b. Defaults to 0.

    Attributes:
        name (str): Name of the function.
        description (str): Short description of the function.
        a (float): Constant parameter a, for use by subclasses.
        b (float): Constant parameter b, for use by subclasses.
    """

    name = ""
    description = ""

    def __init__(self, a=0, b=0):
        self.a = a
        self.b = b

    """Evaluates our arbitrary function f(x).

    Args:
        x (float): Input for function.
    Returns:
        float: The value of f(x).

    """
    @abc.abstractmethod
    def __call__(self, x):
        pass


class Sine(FunctionBase):
    """Function implementation for `f(x) = A * sin(Bx)`."""

    name = "Sine"
    description = "A * sin(Bx)"

    def __call__(self, x):
        return self.a * np.sin(self.b * x)


class Polynomial(FunctionBase):
    """Function implementation for `f(x) = Ax^B`."""

    name = "Polynomial"
    description = "Ax^B"

    def __call__(self, x):
        return self.a * (x ** self.b)


class Mystery(FunctionBase):
    """A mysterious two-parameter function that doesn't have a simple mathematical expression."""

    name = "Mystery"
    description = "Mystery(A, B, x)"

    def __call__(self, x):
        output = 0
        for _ in range(int(self.a * np.sin(x))):
            output += np.cos(x + self.a + self.b)
        return output


if __name__ == "__main__":
    sine = Sine(a=1, b=1)
    print("sin(0) =\t", sine(0.0))

    poly = Polynomial(a=1, b=2)
    print("1 * (5 ** 2) =\t", poly(5))

    mystery = Mystery(a=1.8, b=2.3)
    print("mystery(5) =\t", mystery(5))
