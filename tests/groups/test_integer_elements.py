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

from boring_math.abstract_algebra.protocols.group_element import GroupElement
from boring_math.abstract_algebra.protocols.abelian_group_element import (
    AbelianGroupElement,
)

# Group of additive integers

def sum(m: int, n: int) -> int:
    return m + n


def neg(m: int) -> int:
    return -m


class AdditiveIntegers(AbelianGroupElement[int]):
    pass


class Test_group_addition:
    def test_additive_integers(self) -> None:
        zero = AdditiveIntegers(0, 0, sum, neg)
        one = AdditiveIntegers(1, 0, sum, neg, zero)

        assert zero == zero
        assert one == one
        assert one != zero

        two1 = AdditiveIntegers(2, 0, sum, neg, zero)
        two2 = one + one

        assert two1 == two1
        assert two2 == two2
        assert two1 == two2

        forty_two = AdditiveIntegers(42, 0, sum, neg, zero)

        assert forty_two == one * 42 == 42 * one


# Cyclic group of order 2

def mult2(m: int, n: int) -> int:
    return (m + n) - max(m, n)


def flip(m: int) -> int:
    return (m + 1) % 2


class Ctwo(GroupElement[int]):
    pass


class Test_cyclic_group_order_two:
    def test_cyclic_group_of_order_two(self) -> None:
        one = Ctwo(1, 1, mult2, flip)
        zero = Ctwo(0, 1, mult2, flip)

        assert zero == zero
        assert one == one
        assert one != zero

        assert zero * zero == zero
        assert zero * one == zero
        assert one * zero == zero
        assert one * one == one

        assert zero**42 == zero
        assert one**42 == one
