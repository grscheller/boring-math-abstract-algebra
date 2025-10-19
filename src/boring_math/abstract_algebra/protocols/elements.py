# Copyright 2025 Geoffrey R. Scheller
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
**Protocols for elements of algebraic structures.**

.. note::

    The actual Python datastructures are wrapped in an ``Element``. Protocols are
    used to gear elements to the various types of algebraic systems they can belong.
    Elements are designed to be shared between multiple algebraic structures, like
    a group and another group isomorphic to one of its subgroups.

    Python suffers from a disease introduced by Fortran. Built-in arithmetic operators
    act in a contravariant way while the types themselves are invariant. An ``int``
    added to a ``float`` returns a ``float``. The type system sees the ``int.__add__``
    method as returning an ``int | float | complex``. This presents various typing
    problems and why an underlying data structure is wrapped in an ``Element``.

"""

from typing import Protocol, Self

__all__ = [
    'Element',
    'SemiGroupElement',
    'GroupElement',
    'AbelianSemiGroupElement',
    'AbelianGroupElement',
]


class Element[R](Protocol):
    _representation: R

    def __init__(self, representation: R) -> None: ...
    def __call__(self) -> R:
        return self._representation
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            return False
        if self is other:
            return True
        if self() is other():
            return True
        if self() == other():
            return True
        return False


class SemiGroupElement[R](Element[R], Protocol):
    """An element of a set with a associative binary operator.

    Contract:

        - Multiplication must be associative.

    """
    def __mul__(self, other: Self) -> Self: ...

    def __pow__(self, n: int) -> Self:
        if n > 0:
            g = self
            while n > 1:
                g, n = g * self, n - 1
            return g
        msg = f'For a SemiGroup n>0, but n={n} was given.'
        raise ValueError(msg)

class SemiGroupOne[R](SemiGroupElement[R], Protocol):
    """The unique multiplicative identity, if it exists.

    Contract:

        - Actually a two sided identity.

    """
    ...

class GroupElement[R](SemiGroupElement[R], Protocol):
    """Protocol for a multiplicative group element.

    Contract:

        - Multiplication must be associative.
        - Associate the correct unique multiplicative identity.

    """
    _one: SemiGroupElement[R]

    def __init__(
        self,
        element: SemiGroupElement[R],
        one: SemiGroupElement[R] ,
    ): ...

    def inv(self) -> Self: ...

    def __pow__(self, n: int) -> Self:
        if n > 0:
            g = self
            while n > 1:
                g, n = g * self, n - 1
            return g
        elif n < 0:
            g_inv = self.inv()
            while n < -1:
                g, n = g * g_inv, n + 1
            return g
        else:
            return type(self)._one


class AbelianSemiGroupElement[R](Element[R], Protocol):
    """A set with a commutative, associative binary operator.

    Contract:

        - Addition must be associative and commutative.

    """
    def __init__(self, representatation: R): ...

    def __add__(self, other: Self) -> Self: ...

    def __mul__(self, n: int) -> Self:
        if n > 0:
            g = self
            while n > 1:
                g, n = g + self, n - 1
            return g
        msg = f'For a Abelian SemiGroup n>0, but n={n} was given.'
        raise ValueError(msg)

    def __rmul__(self, n: int) -> Self:
        return self.__mul__(n)


class AbelianGroupElement[R](AbelianSemiGroupElement[R], Protocol):
    """Protocol for an additive (commutative) group element.

    Contract:

        - Addition must be associative and commutative.
        - Associate the correct unique additive identity.

    """
    _zero: AbelianSemiGroupElement[R]

    def __init__(
        self,
        element: AbelianSemiGroupElement[R],
        zero: AbelianSemiGroupElement[R] ,
    ): ...

    def inv(self) -> Self: ...

    def __neg__(self) -> Self:
        return self.inv()

    def __sub__(self, other: Self) -> Self:
        return self + (-other)

    def __mul__(self, n: int) -> Self:
        if n > 0:
            g = self
            while n > 1:
                g, n = g + self, n - 1
            return g
        elif n < 0:
            g = -self
            while n < -1:
                g, n = g - self, n + 1
            return g
        else:
            return type(self)._zero

    def __rmul__(self, n: int) -> Self:
        return self.__mul__(n)
