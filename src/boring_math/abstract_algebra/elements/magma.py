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
**Abstract Magma Element.**

.. info::

    Mathematically a Magma is a set **M** along with a binary
    multiplicative operation **mult: M X M -> M** on that set.

"""

from typing import Callable, Self
from .element import Element

__all__ = ['MagmaElement']


class MagmaElement[M](Element[M]):
    def __init__(
        self,
        representation: M,
        mult: Callable[[M, M], M],
    ) -> None:
        self._mult = mult
        super().__init__(
            representation,
        )

    def __mul__(self, other: Self) -> Self:
        return type(self)(
            self._mult(self(), other()),
            self._mult,
        )


# class MagmaElementAdd[M](Element[M]):
#     def __init__(self, representation: M, operation: Callable[[M, M], M]) -> None:
#         self._add = operation
#         super().__init__(representation)
#
#     def __add__(self, other: Self) -> Self:
#         return type(self)(
#             representation=self._add(self(), other()),
#             operation=self._add,
#         )
