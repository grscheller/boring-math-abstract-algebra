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

.. note::

    The actual Python datastructures are wrapped in an ``Element``. Protocols are
    used to gear elements to the various types of algebraic systems they can belong.
    Elements are designed to be shared between multiple algebraic structures, like
    a group and another group isomorphic to one of its subgroups.

    Python suffers from a disease introduced by Fortran. Built-in arithmetic operators
    act in a contravariant way while the types themselves are invariant. An ``int``
    added to a ``float`` returns a ``float``. The type system sees the ``int.__add__``
    method as returning an ``int | float | complex``. This presents various typing
    problems and why an underlying data structure is wrapped in an ``Element``.

"""

from typing import Callable, Protocol, Self
from .element import Element

__all__ = ['GroupElement']


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
        representation: G,
        identity: G,
        mult: Callable[[G, G], G],
        inverse: Callable[[G], G],
        one: Self | None = None,
    ):
        super().__init__(representation)
        Me = type(me := self)
        Me._identity = identity
        Me._mult = mult
        Me._inverse = inverse
        if mult(identity, identity) != identity:
            msg = 'Contract for the identity was broken.'
            raise ValueError(msg)
        if not mult(self(), identity) == self() == mult(identity, self()):
            msg = 'Contract for the identity was broken.'
            raise ValueError
        if one is None:
            if me() is Me._identity:
                Me.one = me
            else:
                Me.one = Me(
                    identity,
                    identity,
                    mult,
                    inverse,
                    me,
                )
        elif (type(one)._identity, Me._identity) == (identity, identity):
            Me.one = one
        else:
            msg = 'Mult identity given is incompatible.'
            raise ValueError(msg)

    def __mul__(self, g: Self) -> Self:
        Me = type(me := self)
        return type(self)(
            representation=Me._mult(me(), g()),
            identity=Me._identity,
            mult=Me._mult,
            inverse=Me._inverse,
        )

    def invert(self) -> Self:
        Me = type(me := self)
        return Me(
            representation=Me._inverse(me()),
            identity=Me._identity,
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
