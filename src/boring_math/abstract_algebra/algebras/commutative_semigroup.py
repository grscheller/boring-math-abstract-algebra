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
.. admonition:: Additive Semigroup

    Mathematically an Additive Semigroup is a set **S** along with an
    associative binary operation **add: S X S -> S**.

.. important::

    **Contract:** Group initializer parameters must have

    - **add** closed, commutative and associative on reps

"""

from collections.abc import Callable, Hashable
from typing import Self, cast
from pythonic_fp.fptools.function import compose, partial
from .baseset import BaseSet, BaseElement

__all__ = ['CommutativeSemigroup', 'CommutativeSemigroupElement']


class CommutativeSemigroupElement[H: Hashable](BaseElement[H]):
    def __init__(
        self,
        rep: H,
        algebra: 'CommutativeSemigroup[H]',
    ) -> None:
        super().__init__(rep, algebra)

    def __str__(self) -> str:
        """
        :returns: str(self) = CommutativeSemigroupElement<rep>
        """
        return f'CommutativeSemigroupElement<{str(self._rep)}>'

    def __add__(self, other: int | Self) -> Self:
        """
        Add two elements of the same concrete additive semigroup together.

        :param other: Another element within the same additive semigroup or an ``int``.
        :returns: The sum ``self + other``.
        :raises ValueError: If ``self`` and ``other`` are same type but different concrete additive semigroups.
        :raises TypeError: If ``self`` and ``other`` are different types.

        """
        if isinstance(other, type(self)):
            algebra = self._algebra
            if algebra is other._algebra:
                if (add := algebra._add) is not None:
                    return cast(Self, algebra(add(self(), other())))
                else:
                    msg = 'Addition not defined on the algebra of the elements'
                    raise ValueError(msg)
            else:
                msg = 'Addition must be between elements of the same concrete algebra'
                raise ValueError(msg)

        msg = 'Right side of addition wrong type'
        raise TypeError(msg)

    def __radd__(self, other: object) -> Self:
        """
        When left side of addition does not know how to add right side.

        :param other: Left side of the addition.
        :returns: Never returns, otherwise ``left.__add__(right)`` would have worked.
        :raises TypeError: When left side does not know how to add the additive semigroup element.

        """
        msg = 'Left addition operand different type than right'
        raise TypeError(msg)

    def __mul__(self, n: int | Self) -> Self:
        """
        Multiplying additive semigroup element by a positive ``int`` is
        the same as repeated addition.

        :param n: Add additive semigroup element to itself ``n > 0`` times.
        :returns: The sum of the semigroup element n times.
        :raises ValueError: When ``n <= 0``.
        :raises ValueError: If for some reason an add method was not defined on the semigroup.
        """
        if isinstance(n, int):
            if n > 0:
                algebra = self._algebra
                if (add := algebra._add) is None:
                    raise ValueError('Algebra has no addition method')
                r = (r1 := self())
                while n > 1:
                    r, n = add(r1, r), n - 1
                return cast(Self, algebra(r))
            msg = f'For an additive semigroup n>0, but n={n} was given'
            raise ValueError(msg)
        raise ValueError('Element multiplication not defined on algebra')

    def __rmul__(self, n: int) -> Self:
        return self.__mul__(n)


class CommutativeSemigroup[H: Hashable](BaseSet[H]):
    def __init__(
        self,
        add: Callable[[H, H], H],
        narrow: Callable[[H], H] = lambda h: h,
    ) -> None:
        """
        :param add: Closed commutative and associative function reps.
        :param narrow: Narrow the rep type, many-to-one function. Like
                       choosing an element from a coset of a group.

        """
        super().__init__(narrow=narrow)
        self._add = lambda left, right: compose(partial(add, left), narrow)(right)

    def __call__(self, rep: H) -> CommutativeSemigroupElement[H]:
        """
        Add the unique element to the additive semigroup with a given rep.

        :param rep: Representation to add if not already present.
        :returns: The unique element with that representation.

        """
        rep = self._narrow(rep)
        return cast(
            CommutativeSemigroupElement[H],
            self._elements.setdefault(
                rep,
                CommutativeSemigroupElement(rep, self),
            ),
        )
