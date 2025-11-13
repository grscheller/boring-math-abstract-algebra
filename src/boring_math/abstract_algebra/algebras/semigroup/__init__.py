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

        **Contract:** Group initializer parameters must have

        - **mult** closed and associative on reps

"""

from collections.abc import Callable, Hashable
from typing import ClassVar, Final, Self, Type, cast
from ..baseset import BaseSet, BaseElement

__all__ = ['Semigroup', 'SemigroupElement']


class SemigroupElement[H: Hashable](BaseElement[H]):
    def __init__(
        self,
        rep: H,
        algebra: 'Semigroup[H]',
    ) -> None:
        super().__init__(rep, algebra)

    def __mul__(self, other: Self) -> Self:
        """
        .. admonition:: Description.

            Multiply two elements of the same algebra together.

        .. note::

            Have added some runtime type checking. Not really necessary
            if strict typing is used, but may be useful in gradual typing
            situations.

        :param other: Another element within the same algebra.
        :returns: The product ``self * other``.
        :raises ValueError: If ``self`` & ``other`` are same type but different algebras.
        :raises TypeError: If ``self`` & ``other`` are different types.

        """
        if isinstance(other, type(self)):
            algebra = self._algebra
            if algebra is other._algebra:
                if (mult := algebra._mult) is not None:
                    return cast(Self, algebra(mult(self(), other())))
                else:
                    msg = 'Multiplication not defined on the algebra of the elements.'
                    raise ValueError(msg)
            else:
                msg = 'Multiplication must be between elements of the same concrete algebra.'
                raise ValueError(msg)
        msg = 'Right side of multiplication wrong type.'
        raise TypeError(msg)

    def __rmul__(self, other: object) -> Self:
        """
        When left side of multiplication does not know how to multiply right side.

        :param other: Left side of the multiplication.
        :returns: Never returns, otherwise ``left.__mul__(right)`` would have worked.
        :raises TypeError: When left operand does not know how to deal with a SemigroupElement.

        """
        msg = 'Left multiplication operand different type than right.'
        raise TypeError(msg)

    def __pow__(self, n: int) -> Self:
        if n > 0:
            algebra = self._algebra
            if (mult := algebra._mult) is None:
                raise ValueError('Algebra has no multiplication method')
            r = (r1 := self())
            while n > 1:
                r, n = mult(r1, r), n - 1
            return cast(Self, algebra(r))
        msg = f'For a semi-group n>0, but n={n} was given.'
        raise ValueError(msg)


class Semigroup[H: Hashable](BaseSet[H]):
    _Element: ClassVar[Final[Type[SemigroupElement[H]]]] = SemigroupElement

    def __init__(
        self,
        mult: Callable[[H, H], H],
    ):
        super().__init__()
        self._mult = mult
