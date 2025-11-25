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
.. admonition:: Ring

    Mathematically a Ring is an abelian group under addition and a
    Monoid under multiplication. The additive and multiplicative
    identities are denoted ``one`` and ``zero`` respectfully.

    By convention ``one != zero``, otherwise the algebra consists
    of just one unique element.

.. important::

    **Contract:** Ring initializer parameters must have

    - **add** closed, commutative and associative on reps
    - **mult** closed and associative on reps
    - **one** an identity on reps, ``rep*one == rep == one*rep``
    - **zero** an identity on reps, ``rep+zero == rep == zero+rep``
    - **negate** maps ``rep -> -rep``, ``rep + negate(rep) == zero``
    - **zero** ``!=`` **one**

"""

from collections.abc import Callable, Hashable
from typing import Self, cast
from .abelian_group import AbelianGroup, AbelianGroupElement

__all__ = ['Ring', 'RingElement']


class RingElement[H: Hashable](AbelianGroupElement[H]):
    def __init__(
        self,
        rep: H,
        algebra: 'Ring[H]',
    ) -> None:
        super().__init__(rep, cast(AbelianGroup[H], algebra))

    def __str__(self) -> str:
        return f'RingElement[[{str(self._rep)}]]'

    def __mul__(self, other: object) -> Self:
        """
        Multiplication ``*`` operator.

        - Multiplying element by an integer ``n>=0`` is repeated addition.
        - Algebra mult if ``other`` is a member of the same concrete algebra.
        - Otherwise return ``NotImplemented`` (for a right action)

        :param other: Add element to itself ``n >= 0`` times.
        :returns: The sum of the element n times.
        :raises ValueError: if given an element instead of an ``int``.
        :raises ValueError: If add method was not defined on the algebra.

        """
        if isinstance(other, int):
            return super().__mul__(other)

        if isinstance(other, type(self)):
            algebra = self._algebra
            if algebra is other._algebra:
                if (mult := algebra._mult) is not None:
                    return cast(Self, algebra(mult(self(), other())))
                else:
                    msg = 'Multiplication not defined on the algebra'
                    raise ValueError(msg)
            else:
                msg = 'Multiplication must be between elements of the same concrete algebra'
                raise ValueError(msg)

        return NotImplemented

    def __rmul__(self, other: object) -> Self:
        """
        When left side of multiplication does not know how to multiply right side.

        - Multiplying element by an integer ``n>=0`` is repeated addition.
        - If ``other`` not member of same concrete algebra or left mult would of worked.
        - Otherwise return ``NotImplemented`` (for a left action)

        """
        if isinstance(other, int):
            return self.__mul__(other)

        return NotImplemented

    def __pow__(self, n: int) -> Self:
        """
        Raise element to power to the ``int`` power of ``n>=0``.

        :param n: The ``int`` power to raise the element to.
        :returns: The element  raised to a non-negative ``int`` power.
        :raises ValueError: If algebra is not multiplicative.
        :raises ValueError: If algebra does not have a multiplicative identity element.
        :raises ValueError: If ``n < 0``.

        """
        if n >= 0:
            algebra = self._algebra
            if (mult := algebra._mult) is None:
                raise ValueError('Algebra has no multiplication method')
            if (one := algebra._one) is None:
                raise ValueError('Algebra has no multiplicative identity')
            r, r1 = one, self()
            while n > 0:
                r, n = mult(r, r1), n - 1
            return cast(Self, algebra(r))

        msg = f'For a Ring n>=0, but n={n} was given'
        raise ValueError(msg)


class Ring[H: Hashable](AbelianGroup[H]):
    def __init__(
        self,
        add: Callable[[H, H], H],
        mult: Callable[[H, H], H],
        one: H,
        zero: H,
        negate: Callable[[H], H],
        process: Callable[[H], H] = lambda h: h,
    ):
        """
        :param add: Closed commutative and associative function reps.
        :param mult: Closed associative function reps.
        :param one: Representation for multiplicative identity.
        :param zero: Representation for additive identity.
        :param negate: Function mapping element representation to the
                       representation of corresponding negated element.

        """
        super().__init__(add=add, zero=zero, negate=negate, process=process)
        self._mult = mult
        self._one = one

    def __call__(self, rep: H) -> RingElement[H]:
        """
        Add the unique element to the ring with a given rep.

        :param rep: Representation to add if not already present.
        :returns: The unique element with that representation.

        """
        rep = self._process(rep)
        return cast(
            RingElement[H],
            self._elements.setdefault(
                rep,
                RingElement(rep, self),
            ),
        )
