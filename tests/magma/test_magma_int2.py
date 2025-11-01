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

i2_00: Final[Int2] = 0, 0
i2_01: Final[Int2] = 0, 1
i2_10: Final[Int2] = 1, 0
i2_11: Final[Int2] = 1, 1


def xor(u: Int2, v: Int2) -> Int2:
    return (u[0] ^ v[0], u[1] ^ v[1])


magma3: Final[Magma[Int2]] = Magma[Int2](mult=xor)

i00 = magma3(i2_00)
i01 = magma3(i2_01)
i10 = magma3(i2_10)
i11 = magma3(i2_11)


class Test_bool3:
    def test_equality(self) -> None:
        assert i00 * i00 == i00
        assert i00 * i01 == i01
        assert i00 * i10 == i10
        assert i00 * i11 == i11
        assert i01 * i00 == i01
        assert i01 * i01 == i00
        assert i01 * i10 == i11
        assert i01 * i11 == i10
        assert i10 * i00 == i10
        assert i10 * i01 == i11
        assert i10 * i10 == i00
        assert i10 * i11 == i01
        assert i11 * i00 == i11
        assert i11 * i01 == i10
        assert i11 * i10 == i01
        assert i11 * i11 == i00


    def test_identity(self) -> None:
        assert i00 == i00 * i00
        assert i01 == i00 * i01
        assert i10 == i00 * i10
        assert i11 == i00 * i11
        assert i01 == i01 * i00
        assert i00 == i01 * i01
        assert i11 == i01 * i10
        assert i10 == i01 * i11
        assert i10 == i10 * i00
        assert i11 == i10 * i01
        assert i00 == i10 * i10
        assert i01 == i10 * i11
        assert i11 == i11 * i00
        assert i10 == i11 * i01
        assert i01 == i11 * i10
        assert i00 == i11 * i11

    def test_create(self) -> None:
        b_3 = magma3(i2_11)
        b_1 = magma3((0, 1))
        assert b_3 == i11
        assert b_3 is i11
        assert b_1 == i01
        assert b_1 is i01
