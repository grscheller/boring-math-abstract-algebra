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

    Mathematically a Semigroup is a set **S** along with an associative
    binary operation **op: S X S -> S**.

.. important::

    Contract:

    - Multiplication must be associative.

"""

from collections.abc import Callable, Hashable
from typing import ClassVar, Final, Self, Type, cast
from ..magma import Magma, MagmaElement

__all__ = ['Semigroup', 'SemigroupElement']


class SemigroupElement[H: Hashable](MagmaElement[H]):
    def __init__(self, rep: H, algebra: 'Semigroup[H]') -> None:
        super().__init__(rep, algebra)

    def __pow__(self, n: int) -> Self:
        if n > 0:
            algebra = self._algebra
            if (mult := algebra._mult) is None:
                raise ValueError('Algebra has no multiplication method')
            r = (r1 := self())
            while n > 1:
                r, n = mult(r1, r), n - 1
            return cast(Self, algebra(r))
        msg = f'For a semi-group n>0, but n={n} was given.'
        raise ValueError(msg)


class Semigroup[H: Hashable](Magma[H]):
    Element: ClassVar[Final[Type[SemigroupElement[H]]]] = SemigroupElement

    def __init__(self, mult: Callable[[H, H], H]):
        super().__init__(mult)
