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

from boring_math.abstract_algebra.algebras.magma import Magma
from boring_math.abstract_algebra.algebras import Algebra


def non_assoc_mult(m: int, n: int) -> int:
    return m * n - min(m, n)


def non_comm_mult(m: int, n: int) -> int:
    return m * n - m


class Test_magma:
    def test_basic(self) -> None:
        na = Magma[int](mult=non_assoc_mult)
        nc = Magma[int](mult=non_comm_mult)

        na2 = na(2)
        na3 = na(3)

        nc2 = nc(2)
        nc3 = nc(3)
        nc4 = nc(4)

        assert na2() == 2
        assert nc4() == 4
        assert na3() == nc3() == 3

        assert na2 == na2
        assert na2 is na2
        assert na2 != na3
        assert na2 is not na3

        assert nc4 == nc4
        assert nc4 is nc4
        assert nc2 != nc3
        assert nc2 is not nc3

        foo1 = na2 * na3
        foo2 = na3 * na2
        assert foo1 is foo2

        bar1 = nc2 * nc3
        bar2 = nc2 * nc3
        assert bar1 == bar2
        assert bar1 == nc4
        assert bar1() == bar2()
        assert bar1() == nc4()
        assert bar1 is bar2
        assert bar1 is nc4

    def test_illegal_mult(self) -> None:
        na = Magma[int](mult=non_assoc_mult)
        nc = Magma[int](mult=non_comm_mult)
        al = Algebra[int]()

        try:
            what1 = nc(5) * na(6)
        except ValueError as err:
            assert True
            assert str(err) == 'Multiplication must be between elements of the same algebra.'
        else:
            assert what1() == 25
            assert False

        try:
            what2 = na(7) * nc(8)
        except ValueError as err:
            assert str(err) == 'Multiplication must be between elements of the same algebra.'
            assert True
        else:
            assert what2() == 49
            assert False

        try:
            what3 = na(5) * al(25)  # type: ignore
        except TypeError as err:
            assert str(err) == 'Right multiplication operand not part of the algebra.'
            assert True
        else:
            assert what3() == 120
            assert False

        try:
           what4 = al(25) * na(5)
        except TypeError as err:
            assert str(err) == 'Left multiplication operand different type than right.'
            assert True
        else:
            assert what4() == 120
            assert False

        try:
            na(0) * [1,2,3]  # type: ignore
        except TypeError as err:
            assert str(err) == 'Right multiplication operand not part of the algebra.'
            assert True
        else:
            assert False

        try:
            [1,2,3] * na(1)  # type: ignore
        except TypeError as err:
            assert str(err) == 'Left multiplication operand different type than right.'
            assert True
        else:
            assert False
