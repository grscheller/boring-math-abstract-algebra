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
.. admonition:: Group

    Mathematically a Group is a Monoid **G** all of whose elements
    have multiplicative inverses.

.. caution::

    No assumptions are made whether or not the group is Abelian.
    See **AbelianGroup**.

.. important::

    **Contract:** Group initializer parameters must have

    - **mult** closed and associative on reps
    - **one** an identity on reps, ``rep*one == rep == one*rep``
    - **inv** must me idempotent: ``inv(inv(rep)) == rep``

"""

from collections.abc import Hashable
from typing import Callable, ClassVar, Final, cast, Self, Type
from .monoid import Monoid, MonoidElement

__all__ = ['Group', 'GroupElement']


class GroupElement[H: Hashable](MonoidElement[H]):
    def __init__(
        self,
        rep: H,
        algebra: 'Group[H]',
    ) -> None:
        super().__init__(rep, algebra)

    def invert(self) -> Self:
        algebra = self._algebra
        if (invert := algebra._inv) is None:
            raise ValueError('Algebra multiplication not invertable')
        return type(self)(
            invert(self()),
            cast(Group[H], algebra),
        )

    def __pow__(self, n: int) -> Self:
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
        else:
            g = (g_inv := self.invert())
            while n < -1:
                g, n = g * g_inv, n + 1
            return g


class Group[H: Hashable](Monoid[H]):
    _Element: ClassVar[Final[Type[GroupElement[H]]]] = GroupElement[H]

    def __init__(
        self,
        mult: Callable[[H, H], H],
        one: H,
        invert: Callable[[H], H],
    ):
        """
        :param mult: Associative function ``H X H -> H`` on representations.
        :param one: Representation for multiplicative identity.
        :param invert: Function ``H -> H`` mapping element representation to
                       the representation of corresponding inverse element.
        """
        super().__init__(mult, one)
        self._inv = invert
