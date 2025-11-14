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
from typing import Annotated, Any, Literal
from boring_math.abstract_algebra.algebras.additive_semigroup import AdditiveSemigroup

## Infrastructure setup


class HashableNDArrayWrapper:
    __slots__ = '_ndarray', '_array', '_hash', '_shape'

    def __init__(self, ndarray: npt.NDArray[Any]) -> None:
        self._ndarray = np.array(ndarray, copy=True)
        self._ndarray.setflags(write=False)
        self._hash = hash(
            (
                self._ndarray.tobytes(),
                hash((self._ndarray.shape, self._ndarray.dtype)),
            )
        )

    def __call__(self) -> npt.NDArray[Any]:
        return np.array(self._ndarray, copy=True)

    def __hash__(self) -> int:
        return self._hash

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, HashableNDArrayWrapper):
            return NotImplemented
        if (
            self._ndarray.shape != other._ndarray.shape
            or self._ndarray.dtype != other._ndarray.dtype
        ):
            return False
        return np.array_equal(self._ndarray, other._ndarray)


## Implementation

type I64_3x3 = Annotated[HashableNDArrayWrapper[npt.NDArray[np.int64]], Literal[3, 3]]


def matrix_mult(left: I64_3x3, right: I64_3x3) -> I64_3x3:
    return HashableNDArrayWrapper(left() + right())


m3x3 = AdditiveSemigroup[I64_3x3](add=matrix_mult)

np_eye = HashableNDArrayWrapper(np.eye(3, dtype=np.int64))
np_zero = HashableNDArrayWrapper(np.zeros((3, 3), dtype=np.int64))
np_A = HashableNDArrayWrapper(np.array([[5, -1, 0], [0, 2, 1], [1, 3, 1]], dtype=np.int64))
np_B = HashableNDArrayWrapper(np.array([[2, -1, 1], [1, 2 ,0], [2, 3, -1]], dtype=np.int64))
np_C = HashableNDArrayWrapper(np.array([[1, 1, -4], [1, 1, 5], [42, 0, -2]], dtype=np.int64))
np_D = HashableNDArrayWrapper(np.array([[2, -1, 0], [-1, 0, 0], [0, 0, 0]], dtype=np.int64))
np_E = HashableNDArrayWrapper(np.array([[-1, 1, 0], [1, 1, 0], [0, 0, 1]], dtype=np.int64))
np_F = HashableNDArrayWrapper(np.array([[7, -2, 1], [1, 4, 1], [3, 6, 0]], dtype=np.int64))


Eye = m3x3(np_eye)
Zero = m3x3(np_zero)
A = m3x3(np_A)
B = m3x3(np_B)
C = m3x3(np_C)
D = m3x3(np_D)
E = m3x3(np_E)
F = m3x3(np_F)


class Test_bool3:
    def test_equality(self) -> None:
        assert Eye + Zero == Eye
        assert Zero + A == A
        assert B + Zero == B
        assert Zero + Zero == Zero
        assert Zero + E == E
        assert (A + B) + C == A + (B + C)
        assert D + E == Eye
        assert A + B == F

    def test_identity(self) -> None:
        assert D + E is Eye
        assert E + D is D + E
        assert B + Zero is B
        assert Zero + F is F
        assert (A + B) + C is A + (B + C)
        assert D + E is Eye
        assert A + B is F

    def test_create(self) -> None:
        np_see = HashableNDArrayWrapper(np.array([[1, 1, -4], [1, 1, 5], [42, 0, -2]], dtype=np.int64))
        See = m3x3(np_see)
        assert See == C
        assert See is C

    def test_mult(self) -> None:
        Zero*5 == 5*Zero == Zero
        Zero*5 is Zero
        2*D + E*2 == (E+D)*2
        2*E + D*2 is 2*(D+E)
