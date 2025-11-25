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
.. admonition:: Field

    Mathematically a Field is a Commutative Ring all whose non-zero elements
    have multiplicative inverses.

    By convention ``one != zero``, otherwise the algebra consists
    of just one unique element.

.. important::

    **Contract:** Field initializer parameters must have

    - **add** closed, commutative and associative on reps
    - **mult** closed, commutative and associative on reps
    - **zero** an identity on reps, ``rep+zero == rep == zero+rep``
    - **one** an identity on reps, ``rep*one == rep == one*rep``
    - **inv** is the mult inverse function on all non-zero reps
    - **negate** maps ``rep -> -rep``, ``rep + negate(rep) == zero``
    - **invert** maps ``rep -> -rep``, ``rep + negate(rep) == zero``
    - **zero** ``!=`` **one** (by convention)

"""

from collections.abc import Callable, Hashable
from typing import Self, cast
from .ring import Ring, RingElement

__all__ = ['Ring', 'RingElement']


class FieldElement[H: Hashable](RingElement[H]):
    def __init__(
        self,
        rep: H,
        algebra: 'Field[H]',
    ) -> None:
        super().__init__(rep, cast(Ring[H], algebra))

    def __str__(self) -> str:
        return f'FieldElement[[{str(self._rep)}]]'

    def __pow__(self, n: int) -> Self:
        """
        Raise the group element to power to the power of ``n>=0``.

        .. note::

            Have added some runtime type checking so that developers
            do not have to totally depend on their typing tooling.

        :param n: The ``int`` power to raise the element to.
        :returns: The element (or its inverse) raised to an ``int`` power.
        :raises TypeError: If ``self`` and ``other`` are different types.
        :raises ValueError: If ``self`` and ``other`` are same type but different concrete algebras.
        :raises ValueError: If algebra fails to have an identity element.

        """
        algebra = self._algebra
        if (mult := algebra._mult) is None:
            raise ValueError('Algebra has no multiplication method')
        if (one := algebra._one) is None:
            raise ValueError('Algebra has no multiplicative identity')
        if (invert := algebra._inv) is None:
            raise ValueError('Algebra not invertable')
        if n >= 0:
            r, r1 = one, self()
            while n > 0:
                r, n = mult(r, r1), n - 1
            return cast(Self, algebra(r))
        else:
            g = (g_inv := type(self)(invert(self()), cast(Field[H], algebra)))
            while n < -1:
                g, n = g * g_inv, n + 1
            return g


class Field[H: Hashable](Ring[H]):
    def __init__(
        self,
        mult: Callable[[H, H], H],
        add: Callable[[H, H], H],
        one: H,
        zero: H,
        negate: Callable[[H], H],
        invert: Callable[[H], H],
        process: Callable[[H], H] = lambda h: h,
    ):
        """
        :param add: Closed commutative and associative function reps.
        :param mult: Closed associative function reps.
        :param one: Representation for multiplicative identity.
        :param zero: Representation for additive identity.
        :param negate: Function mapping element representation to the
                       representation of corresponding negated element.
        :param invert: Function mapping non-zero element representations
                       to their multiplicative inverses.

        """
        super().__init__(
            mult=mult,
            add=add,
            one=one,
            zero=zero,
            negate=negate,
            process=process,
        )
        self._inv = invert

    def __call__(self, rep: H) -> FieldElement[H]:
        """
        Add the unique element to the ring with a given rep.

        :param rep: Representation to add if not already present.
        :returns: The unique element with that representation.

        """
        rep = self._process(rep)
        return cast(
            FieldElement[H],
            self._elements.setdefault(
                rep,
                FieldElement(rep, self),
            ),
        )
