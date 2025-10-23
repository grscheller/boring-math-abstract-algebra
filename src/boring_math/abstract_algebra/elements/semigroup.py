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
**Protocol for a SemiGroup.**

.. info::

    Mathematically a Semigroup is a set **S** along with an associative
    binary operation **op: S X S -> S**.

.. important::

    The Python ``Semigroup`` protocol extends ``Magma`` by a "contract"
    that ``op`` is associative. 

"""
from abc import abstractmethod
from typing import Callable, Self
from .element import Element

__all__ = [
    'SemigroupElement',
    'SemigroupElementAdditive',
]


class SemigroupElement[S](Element[S]):
    """An element of a set with a associative binary operator.

    Contract:

        - Multiplication must be associative.

    """
    def __init__(self, rep: S, op: Callable[[S, S], S]) -> None:
        super().__init__(rep, op)

    @property
    @abstractmethod
    def ref(self) -> S: ...

    def __mul__(self, other: Self) -> Self:
        Me = type(self)
        return Me(
            rep = Me._op(self.ref, other.ref),
            op = self._op,
        )

    def __pow__(self, n: int) -> Self:
        if n > 0:
            g = self
            while n > 1:
                g, n = g * self, n - 1
            return g
        msg = f'For a SemiGroup n>0, but n={n} was given.'
        raise ValueError(msg)


class SemigroupElementAdditive[S](Element[S]):
    """A set with a commutative, associative binary operator.

    Contract:

        - Addition must be associative and commutative.

    """
    def __init__(self, rep: S, op: Callable[[S, S], S]) -> None:
        super().__init__(rep, op)

    def __add__(self, other: Self) -> Self:
        Me = type(self)
        return Me(
            rep = Me._op(self.ref, other.ref),
            op = self._op,
        )

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
