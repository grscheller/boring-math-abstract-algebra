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
mama: Final[Magma[Bool3]] = Magma[Bool3](mult=xor)

b000, m000 = magma3(b3_000), mama(b3_000)
b001, m001 = magma3(b3_001), mama(b3_001)
b010, m010 = magma3(b3_010), mama(b3_010)
b011, m011 = magma3(b3_011), mama(b3_011)
b100, m100 = magma3(b3_100), mama(b3_100)
b101, m101 = magma3(b3_101), mama(b3_101)
b110, m110 = magma3(b3_110), mama(b3_110)
b111, m111 = magma3(b3_111), mama(b3_111)


class Test_bool3:
    def test_equality(self) -> None:
        assert b000 * b000 == b000
        assert b010 * b011 == b001
        # why???
        moe = b010 * b011
        larry = (curly := b111 * b110)

        assert moe == curly
        assert moe == larry

        assert b111 * b000 == b111
        assert b111 * b111 == b000
        assert b101 * b011 == b110
        assert b110 * b011 == b101

        assert m000 * m000 == m000
        assert m011 * m111 == m100
        assert m111 * m000 == m111
        assert m011 * m110 == m101
        assert m101 * m011 == m110
        assert m111 * m101 == m010

    def test_identity(self) -> None:
        assert b000 * b000 is b000
        assert b010 * b011 is b001
        assert b111 * b000 is b111
        assert b111 * b111 is b000
        assert b101 * b011 is b110
        assert b110 * b011 is b101

        assert m000 * m000 is m000
        assert m011 * m111 is m100
        assert m111 * m000 is m111
        assert m011 * m110 is m101
        assert m101 * m011 is m110
        assert m111 * m101 is m010

    def test_create(self) -> None:
        b_3 = magma3(b3_011)
        b_5 = magma3((True, False, True))
        assert b_3 == b011
        assert b_3 is b011
        assert b_5 == b101
        assert b_5 is b101

        m_4 = mama(b3_100)
        m_1 = mama((False, False, True))
        assert m_4 == m100
        assert m_1 is m001
        assert m_4 == m100
        assert m_1 is m001
