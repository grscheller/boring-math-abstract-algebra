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

from typing import Hashable

__all__ = ['Algebra', 'Element']


class Algebra[H: Hashable]:
    def __init__(self) -> None:
        self.elements: dict[H, Element[H]] = {}

    def __call__(self, rep: H) -> 'Element[H]':
        """Add an element to the algebra with a given representation.

        :param rep: Representation to add if not already present.
        :returns: The element with that representation.

        """
        self.elements.setdefault(rep, Element(rep, self))
        return self.elements[rep]

    def has(self, rep: H) -> bool:
        """Determine if the algebra has a element with a given
        representation.

        :param rep: Element representation.
        :returns: ``True`` if algebra contains an element with with representation ``rep``.

        """
        return rep in self.elements


class Element[R]:
    def __init__(self, rep: R, algebra: Algebra[R]) -> None:
        self._rep = rep
        self._algebra = algebra

    def __call__(self) -> R:
        return self._rep

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            return False
        if self is other:
            return True
        if self() == other():
            return True
        return False
