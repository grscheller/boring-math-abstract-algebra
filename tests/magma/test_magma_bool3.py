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

type Bool3 = tuple[bool, bool, bool]

b3_000: Final[Bool3] = False, False, False
b3_001: Final[Bool3] = False, False, True
b3_010: Final[Bool3] = False, True, False
b3_011: Final[Bool3] = False, True, True
b3_100: Final[Bool3] = True, False, False
b3_101: Final[Bool3] = True, False, True
b3_110: Final[Bool3] = True, True, False
b3_111: Final[Bool3] = True, True, True


def xor(u: Bool3, v: Bool3) -> Bool3:
    return (u[0] ^ v[0], u[1] ^ v[1], u[2] ^ v[2])


magma3: Final[Magma[Bool3]] = Magma[Bool3](mult=xor)

b000 = magma3(b3_000)
b001 = magma3(b3_001)
b010 = magma3(b3_010)
b011 = magma3(b3_011)
b100 = magma3(b3_100)
b101 = magma3(b3_101)
b110 = magma3(b3_110)
b111 = magma3(b3_111)


class Test_bool3:
    def test_equality(self) -> None:
        b000 * b000 == b000
        b010 * b011 == b001
        b111 * b000 == b111
        b111 * b111 == b000
        b101 * b011 == b110 
        b110 * b011 == b101 

    def test_identity(self) -> None:
        b000 * b000 is b000
        b010 * b011 is b001
        b111 * b000 is b111
        b111 * b111 is b000
        b101 * b011 is b110 
        b110 * b011 is b101 

    def test_create(self) -> None:
        b_3 = magma3(b3_011)
        b_5 = magma3((True, False, True))
        b_3 == b011
        b_3 is b011
        b_5 == b101
        b_5 is b101
