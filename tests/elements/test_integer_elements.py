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

from boring_math.abstract_algebra.elements.group import (
    AbelianGroupElement,
    CommutativeGroupElement,
)

# Group of additive integers

def sum(m: int, n: int) -> int:
    return m + n


def neg(m: int) -> int:
    return -m


class AdditiveIntegers(CommutativeGroupElement[int]):
    pass


class Test_group_addition:
    def test_additive_integers(self) -> None:
        zero = AdditiveIntegers(0, 0, sum, neg)
        one = AdditiveIntegers(1, 0, sum, neg)

        assert zero == zero
        assert one == one
        assert one != zero

        two = AdditiveIntegers(2, 0, sum, neg)
        two2 = one + one

        assert two == two
        assert two2 == two2
        assert two == two2

        five = AdditiveIntegers(5, 0, sum, neg)

        assert five == one * 5 == 5 * one
        assert five - two - two == one


# Cyclic group of order 2

def add_mod2(m: int, n: int) -> int:
    return (m + n) % 2


def neg2(m: int) -> int:
    return m % 2


class C2additive(CommutativeGroupElement[int]):
    pass


class C2multiplicative(AbelianGroupElement[int]):
    pass


class Test_cyclic_group_order_two:
    def test_c2_additive(self) -> None:
        zero = C2additive(0, 0, add_mod2, neg2)
        one = C2additive(1, 0, add_mod2, neg2)

        assert zero == zero
        assert one == one
        assert one != zero

        assert zero + zero == zero
        assert zero + one == one
        assert one + zero == one
        assert one + one == zero

        assert zero * 42 == zero == 42 * zero
        assert one * 42 == zero == one * 42
        assert one * 21 == one == one * 21

    def test_c2_multiplicative(self) -> None:
        one = C2multiplicative(0, 0, add_mod2, neg2)
        two = C2multiplicative(1, 0, add_mod2, neg2)

        assert one == one
        assert two == two
        assert two != one

        assert one * one == one
        assert one * two == two
        assert two * one == two
        assert two * two == one

        assert one * 42 == one == 42 * one
        assert two * 42 == one == two * 42
        assert two * 21 == two == two * 21
