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

from typing import Callable
from boring_math.abstract_algebra.algebras.magma.magma import Magma
from boring_math.abstract_algebra.algebras.magma.element import MagmaElement


def non_assoc_mult(m: int, n: int) -> int:
    return m * n - min(m, n)


def non_comm_mult(m: int, n: int) -> int:
    return m * n - m


class MagmaRepInt(Magma[int]):
    def __init__(self, *ms: int, mult: Callable[[int, int], int]) -> None:
        super().__init__(*ms, mult=non_assoc_mult)

na = MagmaRepInt(*range(6), mult=non_assoc_mult)
nc = MagmaRepInt(*range(6), mult=non_comm_mult)

na2 = MagmaElement(2, na)
na3 = MagmaElement(3, na)
na3 = MagmaElement(3, na)
na10 = MagmaElement(10, na)

nc2 = MagmaElement(2, nc)
nc3 = MagmaElement(3, nc)
nc3 = MagmaElement(3, nc)
nc4 = MagmaElement(4, nc)
nc10 = MagmaElement(10, nc)

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

assert (foo := na2 * na3) == (bar := MagmaElement(4, na))
assert foo == bar
assert foo is bar

assert (foo := nc2 * nc3) == (bar := MagmaElement(4, nc))
assert foo == bar
assert foo is bar
assert foo == nc4
assert foo is nc4

# do I want to make elements invariant???

what = nc2 * na2
huh = na2 * nc2
assert what() > 0
assert huh() > 0
