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
.. admonition:: Magma

    Mathematically a Magma is a set **M** along with a binary
    multiplicative operation **mult: M X M -> M** on that set.

.. caution::

    No assumptions are made whether or not the magma multiplication
    is associative. Python's ``*`` operator is used for Magma
    multiplication.

.. important::

    **Contract:** Magma initializer parameters must have

    - **mult** closed on reps

"""

from collections.abc import Callable, Hashable
from typing import Self, cast
from .baseset import BaseSet, BaseElement, NaturalMapping

__all__ = ['Magma', 'MagmaElement']


class MagmaElement[H: Hashable](BaseElement[H]):
    def __init__(
        self,
        rep: H,
        algebra: 'Magma[H]',
    ) -> None:
        super().__init__(rep, algebra)

    def __mul__(self, other: int | Self) -> Self:
        """
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
                    msg = (
                        'Element not part of an algebra where multiplication is defined'
                    )
                    raise ValueError(msg)
            else:
                msg = 'Multiplication must be between elements of the same concrete algebra'
                raise ValueError(msg)

        if isinstance(other, int):
            msg = 'Multiplication by an int on right not defined since addition not defined'
        else:
            msg = 'Right multiplication operand not part of the algebra of left'
        raise TypeError(msg)

    def __rmul__(self, other: object) -> Self:
        """
        For when left operand has no knowledge of the right operand.

        :param other: The left multiplication operand.
        :returns: Never returns, otherwise ``left.__mul__(right)`` would have worked.
        :raises TypeError: When left operand does not know how to deal with a MagmaElement.

        """
        if isinstance(other, int):
            msg = 'Multiplication by an int on left not defined since addition not defined'
        else:
            msg = 'Left multiplication operand different type than right'
        raise TypeError(msg)


class Magma[H: Hashable](BaseSet[H]):

    def __init__(
        self,
        mult: Callable[[H, H], H],
    ) -> None:
        super().__init__()
        self._mult = mult
        self._elements: NaturalMapping[H, MagmaElement[H]] = dict()

    def __call__(self, rep: H) -> MagmaElement[H]:
        return self._elements.setdefault(rep, MagmaElement(rep))
