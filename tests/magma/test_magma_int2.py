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

from typing import Final
from boring_math.abstract_algebra.algebras.magma import Magma

type Int2 = tuple[int, int]

b2_00: Final[Int2] = 0, 0
b2_01: Final[Int2] = 0, 1
b2_10: Final[Int2] = 1, 0
b2_11: Final[Int2] = 1, 1


def xor(u: Int2, v: Int2) -> Int2:
    return (u[0] ^ v[0], u[1] ^ v[1])


magma3: Final[Magma[Int2]] = Magma[Int2](mult=xor)

b00 = magma3(b2_00)
b01 = magma3(b2_01)
b10 = magma3(b2_10)
b11 = magma3(b2_11)


class Test_bool3:
    def test_equality(self) -> None:
        b00 * b00 == b00
        b00 * b01 == b01
        b00 * b10 == b10
        b00 * b11 == b11
        b01 * b00 == b01
        b01 * b01 == b00
        b01 * b10 == b11
        b01 * b11 == b10
        b10 * b00 == b10
        b10 * b01 == b11
        b10 * b10 == b00
        b10 * b11 == b01
        b11 * b00 == b11
        b11 * b01 == b10
        b11 * b10 == b01
        b11 * b11 == b00


    def test_identity(self) -> None:
        b00 == b00 * b00
        b01 == b00 * b01
        b10 == b00 * b10
        b11 == b00 * b11
        b01 == b01 * b00
        b00 == b01 * b01
        b11 == b01 * b10
        b10 == b01 * b11
        b10 == b10 * b00
        b11 == b10 * b01
        b00 == b10 * b10
        b01 == b10 * b11
        b11 == b11 * b00
        b10 == b11 * b01
        b01 == b11 * b10
        b00 == b11 * b11

    def test_create(self) -> None:
        b_3 = magma3(b2_11)
        b_1 = magma3((0, 1))
        b_3 == b11
        b_3 is b11
        b_1 == b01
        b_1 is b01
