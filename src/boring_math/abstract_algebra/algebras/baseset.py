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

"""

from abc import ABC, abstractmethod
from collections.abc import Callable, Container, Hashable, Iterable, Sized
from types import NotImplementedType
from typing import Protocol, Self, runtime_checkable

__all__ = ['BaseSet', 'BaseElement', 'NaturalMapping']


@runtime_checkable
class NaturalMapping[K: Hashable, V](Sized, Iterable[K], Container[K], Protocol):
    """Similar to the collections/abc.Mapping protocol, NaturalMapping
    supports read-only access to dict-like objects which can be extended
    in a "natural" deterministic way.
    """

    def __getitem__(self, key: K) -> V: ...
    def setdefault(self, key: K, default: V) -> V: ...


class BaseElement[H: Hashable]:
    def __init__(
        self,
        rep: H,
        algebra: 'BaseSet[H]',
    ) -> None:
        self._rep = rep
        self._algebra = algebra

    def __call__(self) -> H:
        """
        :returns: The representation wrapped by the element.
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

    def __add__(self, other: Self) -> Self | NotImplementedType:
        return NotImplemented

    def __mul__(self, other: int | Self) -> Self | NotImplementedType:
        return NotImplemented

    def __neg__(self) -> Self:
        msg = 'Negation not defined on the algebra'
        raise TypeError(msg)

    def __pow__(self, n: int) -> Self | NotImplementedType:
        return NotImplemented

    def __sub__(self, other: Self) -> Self | NotImplementedType:
        return NotImplemented

    def __truediv__(self, other: Self) -> Self | NotImplementedType:
        return NotImplemented


class BaseSet[H: Hashable](ABC):

    def __init__(self) -> None:
        self._mult: Callable[[H, H], H] | None = None
        self._add: Callable[[H, H], H] | None = None
        self._one: H | None = None
        self._zero: H | None = None
        self._inv: Callable[[H], H] | None = None
        self._neg: Callable[[H], H] | None = None
        self._sub: Callable[[H], H] | None = None

    @abstractmethod
    def __call__(self, rep: H) -> BaseElement[H]: ...

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
