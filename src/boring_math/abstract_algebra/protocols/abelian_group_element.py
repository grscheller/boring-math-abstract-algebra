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

__all__ = ['AbelianGroupElement']


class AbelianGroupElement[G](Element[G], Protocol):
    """Protocol for a multiplicative group element.

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
        representation: G,
        identity: G,
        add: Callable[[G, G], G],
        negate: Callable[[G], G],
        zero: Self | None = None,
    ):
        super().__init__(representation)
        Me = type(me := self)
        Me._identity = identity
        Me._add = add
        Me._negate = negate
        if add(identity, identity) != identity:
            msg = 'Contract for the identity was broken.'
            raise ValueError(msg)
        if not add(self(), identity) == self() == add(identity, self()):
            msg = 'Contract for the identity was broken.'
            raise ValueError
        if zero is None:
            if me() is Me._identity:
                Me.zero = me
            else:
                Me.zero = Me(
                    identity,
                    identity,
                    add,
                    negate,
                    me,
                )
        elif (type(zero)._identity, Me._identity) == (identity, identity):
            Me.zero = zero
        else:
            msg = 'Mult identity given is incompatible.'
            raise ValueError(msg)

    def __add__(self, g: Self) -> Self:
        Me = type(me := self)
        return type(self)(
            representation=Me._add(me(), g()),
            identity=Me._identity,
            add=Me._add,
            negate=Me._negate,
        )

    def __neg__(self) -> Self:
        Me = type(me := self)
        return Me(
            representation=Me._negate(me()),
            identity=Me._identity,
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
