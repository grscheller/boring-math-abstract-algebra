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
from typing import ClassVar, Final, Self, Type, cast
from .baseset import BaseSet, BaseElement

__all__ = ['AdditiveSemigroup', 'AdditiveSemigroupElement']


class AdditiveSemigroupElement[H: Hashable](BaseElement[H]):
    def __init__(
        self,
        rep: H,
        algebra: 'AdditiveSemigroup[H]',
    ) -> None:
        super().__init__(rep, algebra)

    def __add__(self, other: int | Self) -> Self:
        """
        Add two elements of the same algebra together.

        .. note::

            Have added some runtime type checking. Not really necessary
            if strict typing is used, but may be useful in gradual typing
            situations.

        :param other: Another element within the same algebra.
        :returns: The sum ``self + other``.
        :raises ValueError: If ``self`` & ``other`` are same type but different algebras.
        :raises TypeError: If ``self`` & ``other`` are different types.

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
        :raises TypeError: When left side does not know how to add right.

        """
        msg = 'Left addition operand different type than right'
        raise TypeError(msg)

    def __mul__(self, n: int | Self) -> Self:
        if isinstance(n, int):
            if n > 0:
                algebra = self._algebra
                if (add := algebra._add) is None:
                    raise ValueError('Algebra has no addition method')
                r = (r1 := self())
                while n > 1:
                    r, n = add(r1, r), n - 1
                return cast(Self, algebra(r))
            msg = f'For an additive semi-group n>0, but n={n} was given'
            raise ValueError(msg)
        raise ValueError('Element multiplication not defined on algebra')


class AdditiveSemigroup[H: Hashable](BaseSet[H]):
    _Element: ClassVar[Final[Type[AdditiveSemigroupElement[H]]]] = AdditiveSemigroupElement[H]

    def __init__(
        self,
        add: Callable[[H, H], H],
    ):
        super().__init__()
        self._add = add
