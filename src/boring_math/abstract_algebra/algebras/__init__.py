# Copyright 2024-2025 Geoffrey R. Scheller
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
**Infrastructure for concrete representations of abstract algebras.**

.. note::

    Mathematically speaking, an **Algebra** is a **set** with a collection
    of closed n-ary operators. Usually 1 or 2 binary operations, 0 to 2
    (partial) functions for inverses, and nullary functions for designated
    elements.

.. note::

    **elements:**

    - Elements know the concrete algebra to which they belong.
    - Each element wraps a hashable immutable representation, called a ``rep``.
    - Binary operations like * and + can act on elements.

      - Not their representations.

    **algebras:**

    - Contain a dict of their potential elements.

      - Can be used with potentially infinite or continuous algebras.
      - The dict is "quasi-immutable".

        - Elements are added in a "natural" uniquely deterministic way.

    - Contain user defined functions and attributes.

      - Functions take ``ref`` parameters and return ``ref`` values.
      - Attributes are ``ref`` valued.

    The idea is that

    - An element knows the concrete algebra to which it belongs.
    - Each element wraps a hashable representation, called a ``rep``.
    - There is a one-to-one correspondence between ``rep`` values and elements.
    - Algebra operations act on the elements themselves, not on the reps.
    - Algebras know how to manipulate the representations of their elements.

"""

from collections.abc import Callable, Container, Hashable, Iterable, Sized
from typing import ClassVar, Final, Protocol, Self, Type, runtime_checkable

__all__ = ['BaseAlgebra', 'BaseElement']


@runtime_checkable
class NaturalMapping[K: Hashable, V](Sized, Iterable[K], Container[K], Protocol):
    """Similar to the collections/abc.Mapping protocol, NaturalMapping
    supports read-only access to dict-like objects which can be extended
    in a "natural" deterministic way.
    """

    def __getitem__(self, key: K) -> V: ...
    def setdefault(self, key: K, default: V) -> V: ...


class BaseElement[H: Hashable]:
    def __init__(self, rep: H, algebra: 'BaseSet[H]') -> None:
        self._rep = rep
        self._algebra = algebra

    def __call__(self) -> H:
        return self._rep

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            return False
        if self is other:
            return True
        if self() == other():
            return True
        return False

    def __add__(self, other: Self) -> Self:
        raise NotImplementedError('Addition not defined on algebra.')

    def __mul__(self, other: Self) -> Self:
        raise NotImplementedError('Multiplication not defined on algebra.')

    def __pow__(self, n: int) -> Self:
        raise NotImplementedError('Raising to integer powers not defined on algebra.')


class BaseSet[H: Hashable]:
    Element: ClassVar[Final[Type[BaseElement[H]]]] = BaseElement

    def __init__(self) -> None:
        self._elements: NaturalMapping[H, BaseElement[H]] = dict()
        self._mult: Callable[[H, H], H] | None = None
        self._add: Callable[[H, H], H] | None = None
        self._one: H | None = None
        self._zero: H | None = None
        self._inv: Callable[[H], H] | None = None
        self._neg: Callable[[H], H] | None = None

    def __call__(self, rep: H) -> BaseElement[H]:
        """Add an element to the algebra with a given representation.

        :param rep: Representation to add if not already present.
        :returns: The element with that representation.

        """
        return self._elements.setdefault(rep, type(self).Element(rep, self))

    def __eq__(self, other: object) -> bool:
        # Change to some sort of compatibility condition?
        return self is other

    def has(self, rep: H) -> bool:
        """Determine if the algebra has a element with a given
        representation.

        :param rep: Element representation.
        :returns: ``True`` if algebra contains an element with with representation ``rep``.

        """
        return rep in self._elements
