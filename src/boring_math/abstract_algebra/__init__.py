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
**Abstract Algebra Library.**

A library designed to construct concrete representations for abstract
algebra systems.

- The term "algebra" will be used loosely to mean either,

  - An abstract system unique up to isomorphism.
  - Or a concrete representation of such.

- Each element of the algebra has an internal representation.

  - Each element knows the concrete representation of the algebra to which it belongs.
  - Operations and properties are defined on the algebras themselves.

========== =====================================================================
Module     Description
========== =====================================================================
algebras   Collections of elements with associated operations and relationships.
laws       Assertions for algebras.
protocols  Protocols for algebras.
========== =====================================================================

"""

__author__ = 'Geoffrey R. Scheller'
__copyright__ = 'Copyright (c) 2025 Geoffrey R. Scheller'
__license__ = 'Apache License 2.0'
