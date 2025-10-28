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

from typing import cast, Self
from ..algebra.element import Element
from .magma import Magma

__all__ = ['MagmaElement']


class MagmaElement[M](Element[M]):
    def __init__(self, rep: M, algebra: Magma[M]) -> None:
        self._rep = rep
        self._algebra = algebra

    def __mul__(self, other: Self) -> Self:
        # cast needed since dict is invariant.
        # mypy suggests I use Mapping instead... Mapping???
        algebra = cast(Magma[M], self._algebra)
        return type(self)(
            algebra._mult(self(), other()),
            algebra,
        )
