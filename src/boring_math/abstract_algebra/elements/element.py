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

"""
**Element of an abstract algebra**

.. info::

    Mathematically speaking, an **Algebra** is a **set** with a collection
    of closed n-ary operators. Usually 1 or 2 binary operations, 1 or 0
    partial functions for inverses, and nullary functions for designated
    elements.

"""
__all__ = ['Element']


class Element[R]():
    def __init__(self, representative: R) -> None:
        self._rep = representative

    def __call__(self) -> R:
        return self._rep

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            return False
        if self is other:
            return True
        if self() is other():
            return True
        if self() == other():
            return True
        return False
