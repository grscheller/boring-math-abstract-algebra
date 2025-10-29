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
**Magma**

.. info::

    Mathematically a Magma is a set **M** along with a binary
    multiplicative operation **mult: M X M -> M** on that set.

"""

from typing import Callable, Iterable, Self
from ..algebra.algebra import Algebra, Element


class Magma[M](Algebra[M]):
    def __init__(self, reps: Iterable[M], mult: Callable[[M, M], M]):
        self._mult = mult
        self.elements: dict[M, Element[M]] = {}
        for rep in reps:
            self.elements.setdefault(rep, MagmaElement(rep, self))


class MagmaElement[M](Element[M]):
    def __init__(self, rep: M, algebra: Magma[M]) -> None:
        super().__init__(rep, algebra)

    def __mul__(self, other: Self) -> Self:
        if isinstance((algebra := self._algebra), Magma):
            return type(self)(
                algebra._mult(self(), other()),
                algebra,
        )
        msg = 'Multiplication only defined for subtypes of Magma.'
        raise TypeError(msg)
