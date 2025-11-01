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
**Semigroup**

.. info::

    Mathematically a Semigroup is a set **S** along with an associative
    binary operation **op: S X S -> S**.

.. important::

    Contract:

    - Multiplication must be associative.

"""

from typing import Callable, cast, Self
from ..magma import Magma, MagmaElement


class Semigroup[S](Magma[S]):
    def __init__(self, mult: Callable[[S, S], S]):
        super().__init__(mult)


class SemigroupElement[S](MagmaElement[S]):
    def __init__(self, rep: S, algebra: Semigroup[S]) -> None:
        super().__init__(rep, algebra)

    def __pow__(self, n: int) -> Self:
        if n > 0:
            algebra = cast(Semigroup[S], self._algebra)
            mult = algebra._mult
            r = (r1 := self())
            while n > 1:
                r, n = mult(r1, r), n - 1
            return cast(Self, algebra(r))
        msg = f'For a semi-group n>0, but n={n} was given.'
        raise ValueError(msg)
