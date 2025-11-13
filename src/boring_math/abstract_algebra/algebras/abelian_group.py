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
.. admonition:: Abelian Group

    Mathematically an Abelian Group is a Monoid **G** all of whose
    elements have additive inverses.

.. note::

    Addition is used for the group operation.

.. important::

    **Contract:** AbelianGroup initializer parameters must have

    - **add** closed, associative and commutative on reps
    - **zero** additive identity on reps, ``rep*one == rep == one*rep``
    - **negate** must me idempotent: ``neg(neg(rep)) == rep``

"""

from collections.abc import Hashable
from typing import Callable, ClassVar, Final, cast, Self, Type
from .additive_monoid import AdditiveMonoid, AdditiveMonoidElement

__all__ = ['AbelianGroup', 'AbelianGroupElement']


class AbelianGroupElement[H: Hashable](AdditiveMonoidElement[H]):
    def __init__(
        self,
        rep: H,
        algebra: 'AbelianGroup[H]',
    ) -> None:
        super().__init__(rep, algebra)

    def negate(self) -> Self:
        algebra = self._algebra
        if (negate := algebra._neg) is None:
            raise ValueError('Algebra addition not negatable')
        return type(self)(
            negate(self()),
            cast(AbelianGroup[H], algebra),
        )

    def __mul__(self, n: Self | int) -> Self:
        if isinstance(n, int):
            if n >= 0:
                algebra = self._algebra
                if (add := algebra._add) is None:
                    raise ValueError('Algebra has no multiplication method')
                if (zero := algebra._zero) is None:
                    raise ValueError('Algebra has no multiplicative identity')
                r, r1 = zero, self()
                while n > 0:
                    r, n = add(r, r1), n - 1
                return cast(Self, algebra(r))
            else:
                g = (g_neg := self.negate())
                while n < -1:
                    g, n = g + g_neg, n + 1
                return g
        raise ValueError('Element multiplication not defined on algebra')

    def __rmul__(self, n: int) -> Self:
        return self.__mul__(n)


class AbelianGroup[H: Hashable](AdditiveMonoid[H]):
    _Element: ClassVar[Final[Type[AbelianGroupElement[H]]]] = AbelianGroupElement

    def __init__(
        self,
        add: Callable[[H, H], H],
        zero: H,
        negate: Callable[[H], H],
    ):
        """
        :param add: Associative function ``H X H -> H`` on representations.
        :param zero: Representation for multiplicative identity.
        :param negate: Function ``H -> H`` mapping element representation to
                    the representation of corresponding negated element.
        """
        super().__init__(add, zero)
        self._neg = negate
