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
**Element of an abstract algebra**

.. note::

    The same abstract algebra can be implemented in different ways
    with different types of "representations." The elements themselves
    are callable and return their representations.

    .. important::

        Once set up, the representations and the entities that directly
        act upon them should be thought of as an implementation details.

"""

from typing import Hashable
from ..algebras.algebra import Algebra

__all__ = ['Element']


class Element[R: Hashable]:
    def __init__(self, rep: R, algebra: Algebra[R]) -> None:
        self._rep = rep
        self._algebra = algebra

    def __call__(self) -> R:
        return self._rep

    def __eq__(self, other: object) -> bool:
        if self is other:
            return True
        return False
