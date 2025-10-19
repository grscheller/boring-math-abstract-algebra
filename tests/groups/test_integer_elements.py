# Copyright 2023-2024 Geoffrey R. Scheller
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

from boring_math.abstract_algebra.protocols.elements import (
    AbelianGroupElement,
    AbelianSemiGroupElement,
)

class AddIntSemi(AbelianSemiGroupElement[int]):
    def __init__(self, rep: int):
        self._representation = rep

class AddInt(AbelianGroupElement[int]):
    def __init__(self, element: AddIntSemi, zero: AddIntSemi):
        self._rep = element()
        self._zero = zero

class Test_group_addition:
    def test_abel_int(self) -> None:
        pass # additive 
