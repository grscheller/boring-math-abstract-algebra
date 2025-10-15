# Copyright 2016-2025 Geoffrey R. Scheller
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
**Algebraic Protocols**

.. warning::

    When dealing with built-in numeric types a ``cast`` might still be
    needed. Python suffers from a disease introduced by Fortran.
    Built-in arithmetic operators act in a contravariant way while
    the types themselves are invariant.

    Even though an ``int`` added to an ``int`` will always be
    an ``int``. The ``int.__add__`` method's return type is
    an ``int | float | complex``. As a result ``Self`` cannot
    be used in type signatures.

"""

__all__ = ['orderable_generator']


class Ordered(Protocol):
    def __lt__(self: Self, other: Self) -> bool: ...


class Ring(Protocol):
    def __add__(self: Self, other: Self) -> Self: ...
    def __sub__(self: Self, other: Self) -> Self: ...
    def __mult__(self: Self, other: Self) -> Self: ...
    def __mod__(self: Self, other: Self) -> Self: ...


class OrderedRing(Ordered, Ring, Protocol):
    def __mod__(self: Self, other: Self) -> Self: ...
