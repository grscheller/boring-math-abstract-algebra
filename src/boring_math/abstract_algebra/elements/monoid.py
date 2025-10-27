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
**Abstract Monoid Element.**

.. info::

    Mathematically a Monoid is a Semigroup **M** along with an identity
    element u, that is (∃u ∈ M) => (∀m ∈ M)(u*m = u = m*u).

    Such an identity element is necessarily unique.

"""

from typing import Callable, Self
from .semigroup import SemigroupElement

__all__ = ['MonoidElement']


class MonoidElement[M](SemigroupElement[M]):
    """An element for a Monoid.

    Contract:

        - Multiplication must be associative.

    """

    def __init__(
        self,
        representation: M,
        mult: Callable[[M, M], M],
        one: M,
        /,
    ) -> None:
        self._one = one
        super().__init__(representation, mult)

    def __mul__(self, other: Self) -> Self:
        return type(self)(
            self._mult(self(), other()),
            self._mult,
            self._one,
        )

    def __pow__(self, n: int) -> Self:
        if n >= 0:
            mult = self._mult
            r1 = self()
            r = (one := self._one)
            while n > 0:
                r, n = mult(r, r1), n - 1
            return type(self)(r, mult, one)
        msg = f'For a Monoid n>=0, but n={n} was given.'
        raise ValueError(msg)


# class CommutativeMonoidElement[M](CommutativeSemigroupElement[M]):
#     """A set with a commutative, associative binary operator.
#
#     Contract:
#
#         - Addition must be associative and commutative.
#
#     """
#
#     def __init__(
#         self, representation: M, operation: Callable[[M, M], M], zero: M
#     ) -> None:
#         self._zero = zero
#         super().__init__(representation, operation)
#
#     def __add__(self, other: Self) -> Self:
#         return type(self)(
#             representation=self._add(self(), other()),
#             operation=self._add,
#             zero=self._zero,
#         )
#
#     def __mul__(self, n: int) -> Self:
#         if n >= 0:
#             add = self._add
#             r1 = self()
#             r = self._zero
#             while n > 0:
#                 r, n = add(r, r1), n - 1
#             return type(self)(
#                 representation=r,
#                 operation=add,
#                 zero=self._zero,
#             )
#         msg = f'For a Abelian SemiGroup n>0, but n={n} was given.'
#         raise ValueError(msg)
#
#     def __rmul__(self, n: int) -> Self:
#         return self.__mul__(n)
