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

from typing import cast, Callable, Protocol, Self
from .element import Element

__all__ = [
    'AbelianGroupElement',
    'CommutativeGroupElement',
    'GroupElement',
]


class CommutativeGroupElement[G](Element[G], Protocol):
    """Protocol for an additive group element.

    Contract:

        - Addition must be associative and commutative
        - Associate the correct unique additive identity.

    """

    _identity: G
    _add: Callable[[G, G], G]
    _negate: Callable[[G], G]
    zero: Self

    def __init__(
        self,
        rep: G,
        zero_rep: G,
        add: Callable[[G, G], G],
        negate: Callable[[G], G],
        zero: Self | None = None,
    ):
        super().__init__(rep)
        Me = type(me := self)
        Me._identity = zero_rep
        Me._add = add
        Me._negate = negate
        if add(zero_rep, zero_rep) != zero_rep:
            msg = 'Contract for the identity was broken.'
            raise ValueError(msg)
        if not add(self(), zero_rep) == self() == add(zero_rep, self()):
            msg = 'Contract for the identity was broken.'
            raise ValueError
        if zero is None:
            if me() is Me._identity:
                Me.zero = me
            else:
                Me.zero = Me(
                    zero_rep,
                    zero_rep,
                    add,
                    negate,
                    me,
                )
        elif (type(zero)._identity, Me._identity) == (zero_rep, zero_rep):
            Me.zero = zero
        else:
            msg = 'Mult identity given is incompatible.'
            raise ValueError(msg)

    def __add__(self, g: Self) -> Self:
        Me = type(me := self)
        return type(self)(
            rep=Me._add(me(), g()),
            zero_rep=Me._identity,
            add=Me._add,
            negate=Me._negate,
        )

    def __neg__(self) -> Self:
        Me = type(me := self)
        return Me(
            rep=Me._negate(me()),
            zero_rep=Me._identity,
            add=Me._add,
            negate=Me._negate,
            zero=Me.zero,
        )

    def __sub__(self, g: Self) -> Self:
        return self + (-g)

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


class GroupElement[G](Element[G], Protocol):
    """Protocol for a multiplicative group element.

    Contract:

        - Multiplication must be associative.
        - Associate the correct unique multiplicative identity.

    """

    _identity: G
    _mult: Callable[[G, G], G]
    _inverse: Callable[[G], G]
    one: Self

    def __init__(
        self,
        rep: G,
        one_rep: G,
        mult: Callable[[G, G], G],
        inverse: Callable[[G], G],
        one: Self | None = None,
    ):
        super().__init__(rep)
        Me = type(me := self)
        Me._identity = one_rep
        Me._mult = mult
        Me._inverse = inverse
        if mult(one_rep, one_rep) != one_rep:
            msg = 'Contract for the identity was broken.'
            raise ValueError(msg)
        if not mult(self(), one_rep) == self() == mult(one_rep, self()):
            msg = 'Contract for the identity was broken.'
            raise ValueError
        if one is None:
            if me() is Me._identity:
                Me.one = me
            else:
                Me.one = Me(
                    one_rep,
                    one_rep,
                    mult,
                    inverse,
                    me,
                )
        elif (type(one)._identity, Me._identity) == (one_rep, one_rep):
            Me.one = one
        else:
            msg = 'Mult identity given is incompatible.'
            raise ValueError(msg)

    def __mul__(self, g: Self) -> Self:
        Me = type(me := self)
        return type(self)(
            rep=Me._mult(me(), g()),
            one_rep=Me._identity,
            mult=Me._mult,
            inverse=Me._inverse,
        )

    def invert(self) -> Self:
        Me = type(me := self)
        return Me(
            rep=Me._inverse(me()),
            one_rep=Me._identity,
            mult=Me._mult,
            inverse=Me._inverse,
            one=Me.one,
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
            return type(self).one


class AbelianGroupElement[G](GroupElement[G], Protocol):
    """Protocol for a multiplicative Abelian group element.

    Contract:

        - Multiplication must be associative and commutative..
        - Associate the correct unique multiplicative identity.

    """
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
                msg = 'Only positive integers can act on an Abelian multiplicative group.'
                raise(ValueError(msg))

    def __rmul__(self, h: Self | int) -> Self:
        return self.__mul__(h)
