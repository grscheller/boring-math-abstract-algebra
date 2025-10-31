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
**Abstract Group Element.**

"""

from typing import Callable, Self
from .monoid import MonoidElement

__all__ = [
    'AbelianGroupElement',
    'GroupElement',
]


class GroupElement[G](MonoidElement[G]):
    """Protocol for a multiplicative group element.

    .. important::

        Contract:

        - operation (mult) must be associative
        - one is the representation of the multiplicative identity
        - invert returns the representation of the multiplicative inverse

    """

    def __init__(
        self,
        representation: G,
        operation: Callable[[G, G], G],
        one: G,
        invert: Callable[[G], G],
        /,
    ):
        self._invert = invert
        super().__init__(
            representation,
            operation,
            one,
        )

    def __mul__(self, g: Self) -> Self:
        return type(self)(
            self._mult(self(), g()),
            self._mult,
            self._one,
            self._invert,
        )

    def invert(self) -> Self:
        return type(self)(
            self._invert(self()),
            self._mult,
            self._one,
            self._invert,
        )

    def __truediv__(self, g: Self) -> Self:
        return self * g.invert()

    def __pow__(self, n: int) -> Self:
        if n > 0:
            g = self
            while n > 1:
                g, n = g * self, n - 1
            return g
        elif n < 0:
            g = (g_inv := self.invert())
            while n < -1:
                g, n = g * g_inv, n + 1
            return g
        else:
            return type(self)(
                self._one,
                self._mult,
                self._one,
                self._invert,
            )


class AbelianGroupElement[G](GroupElement[G]):
    """Protocol for a multiplicative group element.

    Contract:

        - operation (mult) must be associative and commutative
        - one is the representation of the multiplicative identity
        - invert returns the representation of the multiplicative inverse

    """

    def __init__(
        self,
        representation: G,
        operation: Callable[[G, G], G],
        one: G,
        invert: Callable[[G], G],
        /,
    ):
        super().__init__(
            representation,
            operation,
            one,
            invert,
        )
