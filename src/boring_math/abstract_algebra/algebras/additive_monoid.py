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
.. admonition:: Additive Monoid

    Mathematically an additive Monoid is a Semigroup **M** along with
    an identity element u, that is (∃u ∈ M) => (∀m ∈ M)(u+m = m+u = m).

    When such an identity element u exists, it is necessarily unique.

.. important::

    **Contract:** Additive Monoid initializer parameters must have

    - **add** closed commutative and associative on reps
    - **zero** an identity on reps, ``rep+zero == rep == zero+rep``

"""

from collections.abc import Callable, Hashable
from typing import ClassVar, Final, Self, Type, cast
from .additive_semigroup import AdditiveSemigroup, AdditiveSemigroupElement

__all__ = ['AdditiveMonoid', 'AdditiveMonoidElement']


class AdditiveMonoidElement[H: Hashable](AdditiveSemigroupElement[H]):
    def __init__(
        self,
        rep: H,
        algebra: 'AdditiveMonoid[H]',
    ) -> None:
        super().__init__(rep, algebra)

    def __mul__(self, n: int | Self) -> Self:
        if isinstance(n, int):
            if n >= 0:
                algebra = self._algebra
                if (add := algebra._add) is None:
                    raise ValueError('Algebra has no multiplication method')
                if (zero := algebra._zero) is None:
                    raise ValueError('Algebra has no multiplicative identity')
                r, r1 = zero, self()
                while n > 0:
                    r, n = add(r, r1), n - 1
                return cast(Self, algebra(r))
            msg = f'For an Additive Monoid n>=0, but n={n} was given'
            raise ValueError(msg)
        raise ValueError('Element multiplication not defined on algebra')


class AdditiveMonoid[H: Hashable](AdditiveSemigroup[H]):
    _Element: ClassVar[Final[Type[AdditiveMonoidElement[H]]]] = AdditiveMonoidElement[H]

    def __init__(
        self,
        add: Callable[[H, H], H],
        zero: H,
    ):
        super().__init__(add=add)
        self._zero = zero
