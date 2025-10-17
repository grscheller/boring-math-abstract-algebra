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
**Algebraic Protocols**

.. warning::

    When dealing with built-in numeric types a ``cast`` might still be
    needed. Python suffers from a disease introduced by Fortran.
    Built-in arithmetic operators act in a contravariant way while
    the types themselves are invariant.

    Even though an ``int`` added to an ``int`` will always be
    an ``int``. The ``int.__add__`` method's return type is
    an ``int | float | complex``. As a result ``Self`` cannot
    be used in type signatures.

"""

from typing import ClassVar, Protocol, Self

__all__ = [
    'Element',
    'SemiGroupElement',
    'One',
    'GroupElement',
    'AbelianSemiGroupElement',
    'Zero',
    'AbelianGroupElement',
    'PartialOrder',
    'TotalOrder',
]


class Element[T]():
    def __init__(self, element: T) -> None:
        self._element = element

    def __call__(self) -> T:
        return self._element


# class SemiGroupElement[T](Element[T], Protocol):
#     """An element of a set with a commutative, associative binary operator.
#
#     Contract: Multiplication must be associative
#
#     """
#     def __init__(self, element: T):
#         self._element = Element(element)
#
#     def element(self) -> Element[T]:
#         return self._element
#
#     def __mult__(self, other: Self) -> Self:
#         return self._element * other._element


class SemiGroupElement[T](Protocol):
    """An element of a set with a commutative, associative binary operator.

    Contract: Multiplication must be associative

    """
    def __mult__(self, other: Self) -> Self: ...


class One[T](Protocol):
    _one: ClassVar[Element[T]]

    def __init__(self, g: Element[T], one: Element[T]): ...

    @classmethod
    def one_element(cls) -> Element[T]:
        return cls._one


class GroupElement[T](SemiGroupElement[T], One[T], Protocol):
    def one(self) -> Self: ...

    def __pow__(self, n: int) -> Self:
        if n > 0:
            g = self
            g_ret = g
            while n > 1:
                g_ret, n = g_ret * g, n - 1
            return g_ret

        if n < 0:
            g_inv = self.inverse()
            g_ret = g_inv
            while n < -1:
                g_ret, n = g_ret * g_inv, n + 1
            return g_ret

        return self.one()


class AbelianSemiGroupElement[T](Protocol):
    """A set with a commutative, associative binary operator.

    Contract: Addition must be associative and commutative.

    """

    def __add__(self, other: Self) -> Self: ...


class Zero[T](Protocol):
    _zero: ClassVar[Element[T]]

    @classmethod
    def zero(cls) -> Element[T]:
        return cls._zero


class AbelianGroupElement[T](AbelianSemiGroupElement[T], Zero[T], Protocol):
    def inverse(self) -> Self: ...

    def __neg__(self) -> Self:
        return self.inverse()

    def __sub__(self, other: Self) -> Self:
        return self + (-other)


class PartialOrder(Protocol):
    """Partially Ordered.

    Contract: Operator ``<=`` is reflexive, anti-symmetric and transitive.

    """

    def __le__(self, other: Self) -> bool: ...


class TotalOrder(PartialOrder, Protocol):
    """Totally Ordered.

    Contract: If overridden, all ordering must be consistently defined
    as a total ordering.

    """

    def __lt__(self, other: Self) -> bool:
        return self <= other and self != other

    def __ge__(self, other: Self) -> bool:
        return not self < other

    def __gt__(self, other: Self) -> bool:
        return not self <= other

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            return False
        if self is other:
            return True
        if self == other:
            return True
        return False
