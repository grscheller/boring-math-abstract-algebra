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

from typing import Annotated, Final, Literal
import numpy as np
import numpy.typing as npt
from boring_math.abstract_algebra.algebras.semigroup import Semigroup

type I64_2x2 = Annotated[npt.NDArray[np.int64], Literal[2, 2]]

def matrix_mult(u: I64_2x2, v: I64_2x2) -> I64_2x2:
    return u @ v

m2x2 = Semigroup[I64_2x2](mult=matrix_mult)

np_eye = np.array([[1, 0], [0, 1]], dtype=np.int64)
np_A = np.array([[5, -1], [0, 2]], dtype=np.int64)
np_B = np.array([[2, -1], [-1, 2]], dtype=np.int64)
np_C = np.array([[1, 1], [1, 1]], dtype=np.int64)
np_D = np.array([[0, 1], [1, 0]], dtype=np.int64)
np_E = np.array([[11, -7], [-2, 4]], dtype=np.int64)

np_eye.flags.writeable = False
np_A.flags.writeable = False
np_B.flags.writeable = False
np_C.flags.writeable = False
np_D.flags.writeable = False
np_E.flags.writeable = False

Eye = m2x2(np_eye)
A = m2x2(np_A)
B = m2x2(np_B)
C = m2x2(np_C)
D = m2x2(np_D)
E = m2x2(np_E)

class Test_bool3:
    def test_equality(self) -> None:
        assert Eye * Eye == Eye
        assert Eye * A == A
        assert B * Eye == B
        assert (A * B) * C == A * (B * C)
        assert D * D == Eye
        assert A * B == E

    def test_identity(self) -> None:
        assert Eye * Eye is Eye
        assert Eye * A is A
        assert B * Eye is B
        assert (A * B) * C is A * (B * C)
        assert D * D is Eye
        assert A * B is E

    def test_create(self) -> None:
        np_see = np.array([[1, 1], [1, 1]], dtype=np.int64)
        np_see.flags.writeable = False
        See = m2x2(np_see)
        assert See == C
        assert See is C
