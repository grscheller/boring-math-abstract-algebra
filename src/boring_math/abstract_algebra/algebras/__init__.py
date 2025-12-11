# Copyright 2024-2025 Geoffrey R. Scheller
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
Boring Math - Abstract Algebra
==============================

.. admonition:: Concrete representations of abstract algebras

    Mathematically speaking, an **Algebra** is a **set** with a collection
    of closed n-ary operators. Usually 1 or 2 binary operations, 0 to 2
    (partial) functions for inverses, and nullary functions for designated
    elements.

    **Element:**

    - Elements know the concrete algebra to which they belong.
    - Each element wraps a hashable immutable representation, called a ``rep``.
    - Binary operations like * and + can act on elements.

    - Not their representations.

    **Algebra:**

    - Contains a dict of potential elements.

    - Can be used with potentially infinite or continuous algebras.
    - The dict is "quasi-immutable".

        - Elements are added in a "natural" uniquely deterministic way.

    - Contain user defined functions and attributes to implement the algebra.

    - Functions take ``ref`` parameters and return ``ref`` values.
    - Attributes are ``ref`` valued.

    The idea is that

    - An element knows the concrete algebra to which it belongs.
    - Each element wraps a hashable representation, called a ``rep``.
    - There is a one-to-one correspondence between ``rep`` values and elements.
    - Algebra operations act on the elements themselves, not on the reps.
    - Algebras know how to manipulate the representations of their elements.

.. admonition:: Laws for algebras

    Ensure concrete representation of abstract algebras adhere to the
    laws (mathematical truths) of the abstract algebra.

    - group laws

.. admonition:: Actions on algebras

    Actions can be performed from either the left or the right leveraging
    the Python multiplication operator ``*``.

.. admonition:: Additional structure on algebras

    Non-algebraic properties for algebras.

    **Orderings**

    - Partial order
    - Total order

.. admonition:: Tools for algebras

    TODO: Make separate PyPI Boring Math projects?

    - groups

      - Sylow tools

    - rings
    - fields

      - Galois tools


"""
