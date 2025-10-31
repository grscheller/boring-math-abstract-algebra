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
**Abstract Ring Element.**

.. info::

    Mathematically a Ring is simultaneously a Monoid **{R, *, one}**
    and a Group **{R, +, zero}** where multiplication is distributive
    over addition.

    By convention we take one != zero, otherwise (∀r ∈ R)(r = one = zero).

"""

from typing import Callable, Self
from .monoid import MonoidElement

__all__ = ['RingElement']


class RingElement[R](MonoidElement[R]):
    """An element for a Ring.

    .. important::

        Contract:

        - mult must be associative
        - one is the representation of the multiplicative identity
        - invert returns the representation of the multiplicative inverse
        - ...

    """

    def __init__(
        self,
        representation: R,
        mult: Callable[[R, R], R],
        one: R,
        add: Callable[[R, R], R],
        zero: R,
        negate: Callable[[R], R],
        invert: Callable[[], R | None],
        /,
    ):
        self._add = add
        self._zero = zero
        self._negate = negate
        super().__init__(
            representation,
            mult,
            one,
        )
        self._invert = invert

    def __mul__(self, g: Self) -> Self:
        return type(self)(
            self._mult(self(), g()),
            self._mult,   # All these must
            self._one,    # be common among
            self._add,    # all the elements
            self._zero,   # making up the ring.
            self._negate,  ## Not sure how to handle these? Functions or values?
            self._invert,  ## Drop this one back to monoid?
        )

    # def invert(self) -> Self:
    #     return type(self)(
    #         self._invert(self()),
    #         self._mult,
    #         self._one,
    #         self._add,
    #         self._zero,
    #         self._negate
    #     )

    # def __truediv__(self, g: Self) -> Self:
    #     return self * g.invert()

    def __pow__(self, n: int) -> Self:
        mult = self._mult
        if n > 0:
            h = (g := self())
            while n > 1:
                h, n = mult(g, h), n - 1
        elif n < 0:
            if (g_inv := self._invert()) is None:
                msg = 'Inverting a non-invertible element.'
                raise ValueError(msg)
            h = g_inv
            while n < -1:
                h, n = mult(h, g_inv), n + 1
        else:
            h = self._one
        return type(self)(
            h,
            self._mult,
            self._one,
            self._add,
            self._zero,
            self._negate,
            self._invert,
        )

