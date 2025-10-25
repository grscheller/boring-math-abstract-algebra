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
**Protocols for elements of algebraic structures.**

"""

from typing import cast, Callable, Self
from .element import Element

__all__ = [
    'AbelianGroupElement',
    'CommutativeGroupElement',
    'GroupElement',
]


class GroupElement[G](Element[G]):
    """Protocol for a multiplicative group element.

    Contract:

        - one is a multiplicative identity
        - mult must be associative
        - invert returns the multiplicative inverse of its argument

    """
    _one: G
    _mult: Callable[[G, G], G]
    _invert: Callable[[G], G]
    one: Self

    def __init__(
        self,
        rep: G,
        one: G,
        mult: Callable[[G, G], G],
        invert: Callable[[G], G],
    ):
        if mult(one, one) != one:
            msg = 'Contract for the identity was broken: mult(one, one) != one.'
            raise ValueError(msg)
        if invert(one) != one:
            msg = 'Contract for the identity was broken: invert(one) != one.'
            raise ValueError(msg)
        if mult(rep, one) != rep:
            msg = 'Contract for the identity was broken: mult(rep, one) != rep'
            raise ValueError(msg)
        if mult(one, rep) != rep:
            msg = 'Contract for the identity was broken: mult(one, rep) != rep'
            raise ValueError(msg)
        if mult(rep, invert(rep)) != one:
            msg = 'Contract for invert was broken: "mult(rep, invert(rep)) != one"'
            raise ValueError(msg)
        if mult(invert(rep), rep) != one:
            msg = 'Contract for the invert was broken: "mult(invert(rep), rep) != one"'
            raise ValueError(msg)

        super().__init__(rep)
        Me = type(self)
        Me._one = one
        Me._mult = mult
        Me._invert = invert

    def __mul__(self, g: Self) -> Self:
        Me = type(me := self)
        return type(self)(
            rep=Me._mult(me(), g()),
            one=Me._one,
            mult=Me._mult,
            invert=Me._invert,
        )

    def invert(self) -> Self:
        Me = type(me := self)
        return Me(
            rep=Me._invert(me()),
            one=Me._one,
            mult=Me._mult,
            invert=Me._invert,
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
            g_inv = self.invert()
            while n < -1:
                g, n = g * g_inv, n + 1
            return g
        else:
            Me = type(self)
            return type(self)(
                rep=Me._one,
                one=Me._one,
                mult=Me._mult,
                invert=Me._invert,
            )


class AbelianGroupElement[G](GroupElement[G]):
    """Protocol for a multiplicative Abelian group element.

    Contract:

        - one is a multiplicative identity
        - mult must be associative and commutative
        - invert returns the multiplicative inverse of its argument

    """

    def __init__(
        self,
        rep: G,
        one: G,
        mult: Callable[[G, G], G],
        invert: Callable[[G], G],
    ):
        #   if mult(rep, ?) != mult(?, rep):
        #       ...
        super().__init__(rep, one, mult, invert)

    def __mul__(self, h: Self | int) -> Self:
        if type(h) is not int:
            return super().__mul__(cast(Self, h))
        else:
            n = h
            if n > 0:
                g = self
                while n > 1:
                    g, n = g * self, n - 1
                return g
            else:
                msg = (
                    'Only positive integers can act on an Abelian multiplicative group.'
                )
                raise (ValueError(msg))

    def __rmul__(self, h: Self | int) -> Self:
        return self.__mul__(h)


class CommutativeGroupElement[G](Element[G]):
    """Protocol for an additive group element.

    Contract:

        - zero is an additive identity
        - add must be associative and commutative
        - negate returns the additive inverse of its argument

    """

    _zero: G
    _add: Callable[[G, G], G]
    _negate: Callable[[G], G]

    def __init__(
        self,
        rep: G,
        zero: G,
        add: Callable[[G, G], G],
        negate: Callable[[G], G],
    ):
        if add(zero, zero) != zero:
            msg = 'Contract for the identity was broken: zero + zero != zero'
            raise ValueError(msg)
        if add(rep, zero) != rep:
            msg = 'Contract for the identity was broken. rep + zero != rep'
            raise ValueError
        if add(zero, rep) != rep:
            msg = 'Contract for the identity was broken. zero + rep != rep'
            raise ValueError

        super().__init__(rep)
        Me = type(self)
        Me._zero = zero
        Me._add = add
        Me._negate = negate

    def __add__(self, g: Self) -> Self:
        Me = type(me := self)
        return type(self)(
            rep=Me._add(me(), g()),
            zero=Me._zero,
            add=Me._add,
            negate=Me._negate,
        )

    def __neg__(self) -> Self:
        Me = type(me := self)
        return Me(
            rep=Me._negate(me()),
            zero=Me._zero,
            add=Me._add,
            negate=Me._negate,
        )

    def __sub__(self, g: Self) -> Self:
        return self + (-g)

    # May want to revisit this if I define group actions elsewhere.
    def __mul__(self, n: int) -> Self:
        if n > 0:
            g = self
            while n > 1:
                g, n = g + self, n - 1
            return g
        elif n < 0:
            g = -self
            while n < -1:
                g, n = g - self, n + 1
            return g
        else:
            return type(self).zero

    def __rmul__(self, n: int) -> Self:
        return self.__mul__(n)
