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
**Infrastructure for an abstract algebra**

.. info::

    Mathematically speaking, an **Algebra** is a **set** with a collection
    of closed n-ary operators. Usually 1 or 2 binary operations, 0 to 2
    (partial) functions for inverses, and nullary functions for designated
    elements.

.. note::

    An instance of the ``Algebra`` class is an implementation of an algebra
    based on the type of the representation for its elements.

    The idea is that

    - Elements wrap representations, called ``reps``.
    - Operations act on the elements themselves, not their representations.
    - Elements know which algebra they belong to.
    - The algebras know how to manipulate the representations of their elements.

"""

# from abc import abstractmethod
from collections.abc import Callable, Container, Hashable, Iterable, Sized
from typing import ClassVar, Protocol, Self, Type, runtime_checkable, reveal_type

__all__ = ['Algebra', 'Element']


@runtime_checkable
class NaturalMapping[K: Hashable, V](Sized, Iterable[K], Container[K], Protocol):
    """Custom type protocol for Mapping-like objects that support
    both read-only access and can be extended in a "natural"
    deterministic way.
    """

    def __getitem__(self, key: K) -> V: ...
    def setdefault(self, key: K, default: V) -> V: ...


class AlgebraElement[H: Hashable]:
    def __init__(self, rep: H, algebra: 'Algebra[H]') -> None:
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
        raise NotImplementedError('Addition not defined on algebra')

    def __mul__(self, other: Self) -> Self:
        raise NotImplementedError('Multiplication not defined on algebra')

    def __pow__(self, n: int) -> Self:
        raise NotImplementedError('Raising to integer powers not defined on algebra')


class Algebra[H: Hashable]:
    Element: ClassVar[Type[AlgebraElement[H]]] = AlgebraElement

    def __init__(self) -> None:
        self._elements: NaturalMapping[H, AlgebraElement[H]] = dict()
        self._mult: Callable[[H, H], H] | None = None
        self._add: Callable[[H, H], H] | None = None
        self._one: H | None = None
        self._zero: H | None = None

    def __call__(self, rep: H) -> AlgebraElement[H]:
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
