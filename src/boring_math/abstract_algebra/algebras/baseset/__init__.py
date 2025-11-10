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
.. admonition:: Implementation Details

    - **BaseSet:** Base class for algebras
    - **BaseElement:** Base class for elements of algebras.

    Even though these class is instantiatable, their purposes are
    to serve as invariant base classes for algebras and algebra elements.

"""

from collections.abc import Callable, Container, Hashable, Iterable, Sized
from typing import ClassVar, Final, Protocol, Self, Type, runtime_checkable

__all__ = ['BaseSet', 'BaseElement']


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
        """
        :returns: a reference to the representation wrapped by the element.
        """
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

    def __neg__(self) -> Self:
        raise NotImplementedError('Negation not defined on algebra.')

    def __pow__(self, n: int) -> Self:
        raise NotImplementedError('Raising to integer powers not defined on algebra.')

    def __sub__(self) -> Self:
        raise NotImplementedError('subtraction not defined on algebra.')

    def __truediv__(self, other: Self) -> Self:
        raise NotImplementedError('division not defined on algebra.')


class BaseSet[H: Hashable]:
    _Element: ClassVar[Final[Type[BaseElement[H]]]] = BaseElement

    def __init__(self) -> None:
        self._elements: NaturalMapping[H, BaseElement[H]] = dict()
        self._mult: Callable[[H, H], H] | None = None
        self._add: Callable[[H, H], H] | None = None
        self._one: H | None = None
        self._zero: H | None = None
        self._inv: Callable[[H], H] | None = None
        self._neg: Callable[[H], H] | None = None

    def __call__(self, rep: H) -> BaseElement[H]:
        """
        .. admonition:: Description

            Add an element to the algebra with a given representation.

        :param rep: Representation to add if not already present.
        :returns: The element with that representation.

        """
        return self._elements.setdefault(rep, type(self)._Element(rep, self))

    def __eq__(self, other: object) -> bool:
        """
        .. warning::

            API subject to change. Might want to make this
            some sort of comparison.

        :param other: Object being compared to. 
        :returns: ``self is other`` if other same type of algebra, otherwise NotImplemented.

        """
        if isinstance(other, type(self)):
            return self is other
        return NotImplemented

    def has(self, rep: H) -> bool:
        """
        Determine if the algebra has a element with a given representation.

        :param rep: Element representation.
        :returns: ``True`` if algebra contains an element with with representation ``rep``.

        """
        return rep in self._elements
