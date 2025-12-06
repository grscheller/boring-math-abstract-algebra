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
.. admonition:: Semigroup

    Mathematically a Semigroup is a set **S** along with an associative
    binary operation **mult: S X S -> S**.

.. important::

    **Contract:** Semigroup initializer parameters must have

    - **mult** closed and associative on reps

"""

from collections.abc import Callable, Hashable
from typing import Self, cast
from pythonic_fp.fptools.function import compose, partial
from .baseset import BaseSet, BaseElement

__all__ = ['Semigroup', 'SemigroupElement']


class SemigroupElement[H: Hashable](BaseElement[H]):
    def __init__(
        self,
        rep: H,
        algebra: 'Semigroup[H]',
    ) -> None:
        super().__init__(rep, algebra)

    def __str__(self) -> str:
        """
        :returns: str(self) = SemigroupElement<rep>

        """
        return f'SemigroupElement<{str(self._rep)}>'

    def __mul__(self, other: object) -> Self:
        """
        Multiply two elements of the same concrete semigroup together.

        :param other: Another element within the same semigroup.
        :returns: The product ``self * other``.
        :raises TypeError: If ``self`` and ``other`` are different types.
        :raises ValueError: If ``self`` and ``other`` are same type but different concrete semigroups.

        """
        if isinstance(other, type(self)):
            algebra = self._algebra
            if algebra is other._algebra:
                if (mult := algebra._mult) is not None:
                    return cast(Self, algebra(mult(self(), other())))
                else:
                    msg = 'Multiplication not defined on the algebra of the elements'
                    raise ValueError(msg)
            else:
                msg = 'Multiplication must be between elements of the same concrete algebra'
                raise ValueError(msg)

        if isinstance(other, int):
            msg = 'Multiplication by an int on right not defined since addition not defined'
            raise TypeError(msg)

        return NotImplemented

    def __rmul__(self, other: object) -> Self:
        """
        When left side of multiplication does not know how to multiply right side.

        :param other: Left side of the multiplication.
        :returns: NotImplemented, otherwise ``left.__mul__(right)`` would have worked.
        :raises TypeError: When multiplying on left by an int.

        """
        if isinstance(other, int):
            msg = 'Multiplication by an int on left not defined since addition not defined'
            raise TypeError(msg)

        return NotImplemented

    def __pow__(self, n: int) -> Self:
        """
        Raising semigroup element to a positive ``int`` power is
        the same as repeated multiplication.

        :param n: Multiply semigroup element to itself ``n > 0`` times.
        :returns: The product of the semigroup element n times.
        :raises ValueError: When ``n <= 0``.
        :raises ValueError: If for some reason a mult method was not defined on the semigroup.
        """
        if n > 0:
            algebra = self._algebra
            if (mult := algebra._mult) is None:
                raise ValueError('Algebra has no multiplication method')
            r = (r1 := self())
            while n > 1:
                r, n = mult(r1, r), n - 1
            return cast(Self, algebra(r))
        msg = f'For a semigroup n>0, but n={n} was given'
        raise ValueError(msg)


class Semigroup[H: Hashable](BaseSet[H]):

    def __init__(
        self,
        mult: Callable[[H, H], H],
        narrow: Callable[[H], H] = lambda h: h,
    ) -> None:
        """
        :param mult: Associative function ``H X H -> H`` on representations.
        :param narrow: Narrow the rep type, many-to-one function. Like
                       choosing an element from a coset of a group.

        """
        super().__init__(narrow=narrow)
        self._mult = lambda left, right: compose(partial(mult, left), narrow)(right)

    def __call__(self, rep: H) -> SemigroupElement[H]:
        """
        Add the unique element to the semigroup with a given rep.
 
        :param rep: Representation to add if not already present.
        :returns: The unique element with that representation.
 
        """
        rep = self._narrow(rep)
        return cast(
            SemigroupElement[H],
            self._elements.setdefault(
                rep, SemigroupElement(rep, self),
            ),
        )
