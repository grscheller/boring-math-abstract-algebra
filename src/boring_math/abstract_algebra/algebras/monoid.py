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
.. admonition:: Monoid

    Mathematically a Monoid is a Semigroup **M** along with an identity
    element u, that is (∃u ∈ M) => (∀m ∈ M)(u*m = m*u = m).

    When such an identity element u exists, it is necessarily unique.

.. important::

    **Contract:** Monoid initializer parameters must have

    - **mult** closed and associative on reps
    - **one** an identity on reps, ``rep*one == rep == one*rep``

"""

from collections.abc import Callable, Hashable
from typing import Self, cast
from .semigroup import Semigroup, SemigroupElement

__all__ = ['Monoid', 'MonoidElement']


class MonoidElement[H: Hashable](SemigroupElement[H]):
    def __init__(
        self,
        rep: H,
        algebra: 'Monoid[H]',
    ) -> None:
        super().__init__(rep, cast(Semigroup[H], algebra))

    def __str__(self) -> str:
        return f'MonoidElement[[{str(self._rep)}]]'

    def __pow__(self, n: int) -> Self:
        """
        Raise the group element to power to the power of ``n>=0``.

        :param n: The ``int`` power to raise the element to.
        :returns: The element (or its inverse) raised to an ``int`` power.
        :raises TypeError: If ``self`` and ``other`` are different types.
        :raises ValueError: If ``self`` and ``other`` are same type but different concrete groups.
        :raises ValueError: If algebra fails to have an identity element.

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
        msg = f'For a Monoid n>=0, but n={n} was given'
        raise ValueError(msg)


class Monoid[H: Hashable](Semigroup[H]):
    def __init__(
        self,
        mult: Callable[[H, H], H],
        one: H,
    ):
        """
        :param mult: Associative function ``H X H -> H`` on representations.
        :param one: Representation for multiplicative identity.
        :returns: A monoid algebra.

        """
        super().__init__(mult=mult)
        self._one = one

    def __call__(self, rep: H) -> MonoidElement[H]:
        """
        Add the unique element to the monoid with a given rep.

        :param rep: Representation to add if not already present.
        :returns: The unique element with that representation.

        """
        return cast(
            MonoidElement[H],
            self._elements.setdefault(
                rep,
                MonoidElement(rep, self),
            ),
        )
