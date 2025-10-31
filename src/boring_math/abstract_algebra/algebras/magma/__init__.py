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
**Magma**

.. info::

    Mathematically a Magma is a set **M** along with a binary
    multiplicative operation **mult: M X M -> M** on that set.

.. note::
    Python ``dict`` is invariant. It is used to represents
    the underlying **set** of elements of the **magma**. Python
    typing does not allow it to be declared a Mapping because
    the ``dict.setdefault`` method is not part of Mapping. 

    Since elements are added to the ``dict`` in a completely
    deterministic "natural" way and are never changed or deleted
    once added, and elements are never returned to client code
    without adding them to the ``dict``, the maintainer feels
    the use of ``cast`` in this module's code is justified.

"""

from typing import Callable, cast, Self
from .. import Algebra, Element


class Magma[M](Algebra[M]):
    def __init__(self, mult: Callable[[M, M], M]) -> None:
        super().__init__()
        self._mult = mult

    def __call__(self, rep: M) -> 'MagmaElement[M]':
        """Add an element to the algebra with a given representation.

        :param rep: Representation to add if not already present.
        :returns: The element with that representation.

        """
        self.elements.setdefault(rep, MagmaElement(rep, self))
        return cast('MagmaElement[M]', self.elements[rep])


class MagmaElement[M](Element[M]):
    def __init__(self, rep: M, algebra: Magma[M]) -> None:
        super().__init__(rep, algebra)

    def __mul__(self, other: Self) -> Self:
        """Multiply two elements of the same algebra together.

        .. note::
            Have added some runtime type checking. Not necessary if
            strict typing is used, but may be useful in gradual typing
            situations.

        :param other: Another element within the same algebra.
        :returns: The product ``self * other``.
        :raises ValueError: If ``self`` & ``other`` are same type but different algebras.
        :raises TypeError: If ``self`` & ``other`` are different types.

        """
        if isinstance(other, type(self)):
            algebra = cast(Magma[M], self._algebra)
            if algebra is other._algebra:
            #   return cast(Self, algebra(algebra._mult(self(), other())))
                return cast(Self, algebra(algebra._mult(self(), other())))
            else:
                msg = 'Multiplication must be between elements of the same algebra.'
                raise ValueError(msg)
        msg = 'Right multiplication operand not part of the algebra.'
        raise TypeError(msg)

    def __rmul__(self, other: object) -> Self:
        """For when left operand has no knowledge of the right operand.

        :param other: The left multiplication operand.
        :returns: Never returns, otherwise ``left.__mul__(right)`` would have.
        :raises TypeError:

        """
        msg = 'Left multiplication operand different type than right.'
        raise TypeError(msg)
