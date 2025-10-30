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

from typing import Callable, Iterable
from boring_math.abstract_algebra.algebras.magma import Magma


def non_assoc_mult(m: int, n: int) -> int:
    return m * n - min(m, n)


def non_comm_mult(m: int, n: int) -> int:
    return m * n - m


class MagmaRepInt(Magma[int]):
    def __init__(self, ms: Iterable[int], mult: Callable[[int, int], int]) -> None:
        super().__init__(ms, mult=non_assoc_mult)

class Test_magma:
    def test_basic(self) -> None:
        na = MagmaRepInt(range(7), mult=non_assoc_mult)
        nc = MagmaRepInt(range(7), mult=non_comm_mult)

        na2 = na(2)
        na3 = na(3)
        na4 = na(4)
        na5 = na(5)
        na6 = na(6)
        na10 = na(25)

        nc2 = nc(2)
        nc3 = nc(3)
        nc4 = nc(4)
        nc5 = nc(5)
        nc6 = nc(6)
        nc10 = nc(10)

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
        assert foo1 == foo2
#       assert foo1 is foo2

        bar1 = nc2 * nc3
        bar2 = nc2 * nc(3)
        assert bar1 == nc4
        assert bar1 == bar2
        assert bar1 is nc4
        assert bar1 is bar2

        # Do I want to make elements invariant???
        # No, they are the same type.
        # Blow up if algebras not the same? Make algebra a singleton?
        # huh = nc3 * na2
        # what = nc3 * na2
        # assert huh() == 4
        # assert what() == 3
