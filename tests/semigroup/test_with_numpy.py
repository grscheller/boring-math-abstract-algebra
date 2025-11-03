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

import numpy as np
import numpy.typing as npt
from typing import Annotated, Any, Literal, reveal_type
from boring_math.abstract_algebra.algebras.semigroup import Semigroup

## Infrastructure setup


class HashableNDArray:
    __slots__ = '_array', '_hash', '_shape'

    def __init__(self, array: npt.NDArray[Any]) -> None:
        self._array = np.array(array, copy=True)
        self._array.setflags(write=False)
        self._hash = hash((
            self._array.tobytes(),
            hash((
                self._array.shape,
                self._array.dtype,
                )),
            ))

    def __call__(self) -> npt.NDArray[Any]:
        return np.array(self._array, copy=True)

    def __hash__(self) -> int:
        return self._hash

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, HashableNDArray):
            return NotImplemented
        if self._array.shape != other._array.shape or self._array.dtype != other._array.dtype:
            return False
        return np.array_equal(self._array, other._array)


## Implementation

type I64_2x2 = Annotated[HashableNDArray[npt.NDArray[np.int64]], Literal[2, 2]]


def matrix_mult(left: I64_2x2, right: I64_2x2) -> I64_2x2:
    return HashableNDArray(left() @ right())

m2x2 = Semigroup[I64_2x2](mult=matrix_mult)

reveal_type(m2x2)

np_eye = HashableNDArray(np.identity(2, dtype=np.int64))
np_zero = HashableNDArray(np.zeros((2, 2), dtype=np.int64))
np_A = HashableNDArray(np.array([[5, -1], [0, 2]], dtype=np.int64))
np_B = HashableNDArray(np.array([[2, -1], [-1, 2]], dtype=np.int64))
np_C = HashableNDArray(np.array([[1, 1], [1, 1]], dtype=np.int64))
np_D = HashableNDArray(np.array([[0, 1], [1, 0]], dtype=np.int64))
np_E = HashableNDArray(np.array([[11, -7], [-2, 4]], dtype=np.int64))

reveal_type(np_eye)

Eye = m2x2(np_eye)
Zero = m2x2(np_zero)
A = m2x2(np_A)
B = m2x2(np_B)
C = m2x2(np_C)
D = m2x2(np_D)
E = m2x2(np_E)

reveal_type(Eye)


class Test_bool3:
    def test_equality(self) -> None:
        assert Eye * Eye == Eye
        assert Eye * A == A
        assert B * Eye == B
        assert E * Zero == Zero
        assert Zero *  E == Zero
        assert (A * B) * C == A * (B * C)
        assert D * D == Eye
        assert A * B == E

    def test_identity(self) -> None:
        assert Eye * Eye is Eye
        assert Eye * A is A
        assert B * Eye is B
        assert E * Zero is Zero
        assert Zero *  E is Zero
        assert (A * B) * C is A * (B * C)
        assert D * D is Eye
        assert A * B is E

    def test_create(self) -> None:
        np_see = HashableNDArray(np.array([[1, 1], [1, 1]], dtype=np.int64))
        See = m2x2(np_see)
        assert See == C
        assert See is C

    def test_pow(self) -> None:
        Eye ** 5 == Eye
        Eye ** 5 is Eye
