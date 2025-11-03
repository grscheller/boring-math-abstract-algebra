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
**Monoid**

.. info::

    Mathematically a Monoid is a Semigroup **M** along with an identity
    element u, that is (∃u ∈ M) => (∀m ∈ M)(u*m = m*u = m).

    Such an identity element u exists, it is necessarily unique.

.. important::

    Contract:

    - Semigroup multiplication consistent with the identity element.

"""

from typing import Callable, cast, Self
from ..semigroup import Semigroup, SemigroupElement


class Monoid[M](Semigroup[M]):
    def __init__(self, mult: Callable[[M, M], M], one: M):
        super().__init__(mult)
        self._one = one


class MonoidElement[M](SemigroupElement[M]):
    def __init__(self, rep: M, algebra: Monoid[M]) -> None:
        super().__init__(rep, algebra)

    def __pow__(self, n: int) -> Self:
        if n >= 0:
            algebra = cast(Monoid[M], self._algebra)
            mult = algebra._mult
            r, r1 = algebra._one, self()
            while n > 0:
                r, n = mult(r, r1), n - 1
            return type(self)(r, algebra)
        msg = f'For a Monoid n>=0, but n={n} was given.'
        raise ValueError(msg)
