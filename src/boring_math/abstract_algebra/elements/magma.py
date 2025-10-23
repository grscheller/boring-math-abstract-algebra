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
**Protocol for a Magma.**

.. info::

    Mathematically a Magma is a set **M** along with a binary
    operation **op: M X M -> M**.

.. important::

    The Python ``Magma`` protocol wraps a Python hashable values of type ``R``
    along with an operation ``op: Callable[[R, R], R]``. The **set** making
    up the elements of the **Magma** will be implemented as a Python ``dict``
    whose keys are the underlying values of the data structures making up
    the elements of the Magma.

.. note::

    Python suffers from a disease introduced by Fortran. Built-in arithmetic
    operators act in a contravariant way while the types themselves are not
    quite invariant. An ``int`` added to a ``float`` returns a ``float``.
    The type system sees the ``int.__add__`` method as returning an
    ``int|float|complex`` despite an ``int`` added to an ``int`` always
    returning an ``int``. This presenting various typing challenges.

"""

from typing import Callable, Self
from .element import Element

__all__ = ['MagmaElement']


class MagmaElement[M](Element[M]):

    def __init__(self, rep: M, op: Callable[[M, M], M] | None = None) -> None:
        if op is not None:
            if type(self)._op is not op:
                msg = 'MagmaElement: Operation already asigned.'
                raise ValueError(msg)
            type(self)._op = op

    def __mul__(self, other: Self) -> Self:
        Me = type(self)
        return Me(
            rep = Me._op(self.ref, other.ref),
            op = self._op,
        )
