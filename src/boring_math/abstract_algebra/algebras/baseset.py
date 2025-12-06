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


class BaseElement[H: Hashable](ABC):
    def __init__(
        self,
        rep: H,
        algebra: 'BaseSet[H]',
    ) -> None:
        self._rep = algebra._narrow(rep)
        self._algebra = algebra

    @abstractmethod
    def __str__(self) -> str:
        """
        :returns: str(self) = AlgebraElement<rep>
        """
        ...

    def __call__(self) -> H:
        """
        .. warning::

            A trade off is being made in favor of efficiency over
            encapsulation. An actual reference to the wrapped ``rep``
            is returned to eliminate the overhead of a copy.

        :returns: The narrowed representation wrapped within the element.

        """
        return self._rep

    def __eq__(self, other: object) -> bool:
        """
        Compares if two elements, not necessarily in the same concrete
        algebra, contain the same representations.

        .. warning::

            Any sort of difference in rep narrowing is not taken into
            consideration.

        :param other: Object to be compared with.
        :returns: True if both are elements and the reps compare as equal
                  and are of the same invariant type.

        """
        if not isinstance(other, type(self)):
            return False
        if self is other:
            return True
        if (rep_self := self()) == (rep_other := other()):
            if type(rep_self) is type(rep_other):
                return True
        return False

    def __add__(self, other: Self) -> Self | NotImplementedType:
        return NotImplemented

    def __mul__(self, other: int | Self) -> Self | NotImplementedType:
        return NotImplemented

    def __pow__(self, n: int) -> Self | NotImplementedType:
        return NotImplemented

    def __neg__(self) -> Self:
        msg = 'Negation not defined on the algebra'
        raise TypeError(msg)

    def __sub__(self, other: Self) -> Self | NotImplementedType:
        return NotImplemented

    def __truediv__(self, other: Self) -> Self | NotImplementedType:
        return NotImplemented


class BaseSet[H: Hashable](ABC):
    def __init__(self, narrow: Callable[[H], H] = lambda h: h) -> None:
        self._narrow: Callable[[H], H] = narrow
        self._elements: NaturalMapping[H, BaseElement[H]] = dict()
        self._mult: Callable[[H, H], H] | None = None
        self._one: H | None = None
        self._inv: Callable[[H], H] | None = None
        self._add: Callable[[H, H], H] | None = None
        self._zero: H | None = None
        self._neg: Callable[[H], H] | None = None

    @abstractmethod
    def __call__(self, rep: H) -> BaseElement[H]:
        """
        Add the unique element in the algebra with a given rep.
        """
        ...

    def __eq__(self, other: object) -> bool:
        """
        Compare if two algebras are the same concrete algebra.

        :param other: Object being compared to.
        :returns: True only if other is same concrete algebra, False if
                  a different concrete algebra, otherwise NotImplemented.

        """
        if isinstance(other, type(self)):
            return self is other
        return NotImplemented

    def narrow(self, rep: H) -> H:
        return self._narrow(rep)
