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
**Protocols for orderings of algebraic structures.**

"""

from typing import Protocol, Self

__all__ = [
    'PartialOrder',
    'TotalOrder',
]


class PartialOrder(Protocol):
    """Partially Ordered.

    Contract: Operator ``<=`` is reflexive, anti-symmetric and transitive.

    """

    def __le__(self, other: Self) -> bool: ...


class TotalOrder(PartialOrder, Protocol):
    """Totally Ordered.

    Contract: If overridden, all ordering must be consistently defined
    as a total ordering.

    """

    def __lt__(self, other: Self) -> bool:
        return self <= other and self != other

    def __ge__(self, other: Self) -> bool:
        return not self < other

    def __gt__(self, other: Self) -> bool:
        return not self <= other

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            return False
        if self is other:
            return True
        if self == other:
            return True
        return False
