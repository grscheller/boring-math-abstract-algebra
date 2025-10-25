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
**Abstract Semigroup Elements.**

.. info::

    Mathematically a Semigroup is a set **S** along with an associative
    binary operation **op: S X S -> S**.

"""
from typing import Callable, Self
from .magma import MagmaElementMult, MagmaElementAdd

__all__ = [
    'AbelianSemigroupElement',
    'CommutativeSemigroupElement',
    'SemigroupElement',
]


class SemigroupElement[S](MagmaElementMult[S]):
    """An element of a set with a associative binary operator.

.. important::

    Contract:

    - Multiplication must be associative.

    """
    def __init__(self, representation: S, operation: Callable[[S, S], S]) -> None:
        super().__init__(representation, operation)

    def __pow__(self, n: int) -> Self:
        if n > 0:
            mult = self._mult
            r = (r1 := self())
            while n > 1:
                r, n = mult(r1, r), n - 1
            return type(self)(r, mult)
        msg = f'For a semi-group n>0, but n={n} was given.'
        raise ValueError(msg)


class AbelianSemigroupElement[S](SemigroupElement[S]):
    """An element of a set with a associative binary operator.

    .. important::

        Contract:

        - Multiplication must also be commutative.

    """
    pass


class CommutativeSemigroupElement[S](MagmaElementAdd[S]):
    """A set with a commutative, associative binary operator.

    .. important::

        Contract:

        - Addition must be associative and commutative.

    """
    def __init__(self, representation: S, operation: Callable[[S, S], S]) -> None:
        super().__init__(representation, operation)

    def __mul__(self, n: int) -> Self:
        if n > 0:
            add = self._add
            r = (r0 := self())
            while n > 1:
                r, n = add(r0, r), n - 1
            return type(self)(r, add)
        msg1 = 'Commutative semi-group integer mult makes sense only for n>0,'
        msg2 = f' but n={n} was given.'
        raise ValueError(msg1 + msg2)

    def __rmul__(self, n: int) -> Self:
        return self.__mul__(n)
