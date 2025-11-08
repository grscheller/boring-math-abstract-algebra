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
.. note::

    Mathematically a Monoid is a Semigroup **M** along with an identity
    element u, that is (∃u ∈ M) => (∀m ∈ M)(u*m = m*u = m).

    When such an identity element u exists, it is necessarily unique.

.. important::

    Contract:

    - Semigroup multiplication consistent with the identity element.

"""

from collections.abc import Hashable
from typing import Callable, ClassVar, Final, Self, Type, cast
from ..semigroup import Semigroup, SemigroupElement

__all__ = ['Monoid', 'MonoidElement']


class MonoidElement[H: Hashable](SemigroupElement[H]):
    def __init__(self, rep: H, algebra: 'Monoid[H]') -> None:
        super().__init__(rep, algebra)

    def __pow__(self, n: int) -> Self:
        if n >= 0:
            algebra = self._algebra
            if (mult := algebra._mult) is None:
                raise ValueError('Algebra has no multiplication method')
            if (one := algebra._one) is None:
                raise ValueError('Algebra has no multiplicative identity')
            r, r1 = one, self()
            while n > 0:
                r, n = mult(r, r1), n - 1
            return cast(Self, algebra(r))
        msg = f'For a Monoid n>=0, but n={n} was given.'
        raise ValueError(msg)


class Monoid[H: Hashable](Semigroup[H]):
    Element: ClassVar[Final[Type[MonoidElement[H]]]] = MonoidElement

    def __init__(self, mult: Callable[[H, H], H], one: H):
        super().__init__(mult)
        self._one = one
