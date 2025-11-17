# Copyright 2025 Geoffrey R. Scheller
#
# Licensed under the Apache License, Version 2.0 (the "License")
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

import re
from typing import Self
from boring_math.abstract_algebra.algebras.commutative_monoid import CommutativeMonoid

## First define infrastructure

# Define hashable representation type and functions on this type


class AB:
    def __init__(self, ab: str):
        self._pat = (pat := re.compile('[ab]*'))
        if pat.fullmatch(ab) is None:
            msg = f"Representation string {ab} contains characters other than 'a' or 'b'"
            raise ValueError(msg)
        rep, it = '', iter(ab)
        try:
            r0 = next(it)
            rep += r0
            while True:
                while r0 == (r1 := next(it)):
                    continue
                rep, r0 = rep + r1, r1
        except StopIteration:
            pass
        self._rep = rep
        self._hash = hash(rep)

    def __hash__(self) -> int:
        return self._hash

    def __len__(self) -> int:
        return len(self._rep)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            return NotImplemented
        if self._rep == other._rep:
            return True
        return False

    def __add__(self, other: Self) -> 'AB':
        if len(self) > 0 and len(other) > 0 and self._rep[-1] == self._rep[0]:
            return AB(self._rep[0:-1]) + AB(other._rep[1:])
        return AB(self._rep + other._rep)


def ab_add(left: AB, right: AB) -> AB:
    return left + right


# Define an algebra where consecutive elements don't repeat

ab_alg = CommutativeMonoid[AB](add=ab_add, zero=AB(''))


## Test above infrastructure


class TestAB:
    def test_equality_identity(self) -> None:
        assert AB('') == AB('')
        assert AB('') is not AB('')
        assert AB('aaabb') == AB('ab')
        assert AB('aaabb') is not AB('ab')

    def test_add(self) -> None:
        assert AB('') + AB('') == AB('')
        assert AB('') + AB('abab') == AB('abab')
        assert AB('baba') + AB('') == AB('bbbabbaaa')
        assert AB('baaa') + AB('aaabb') == AB('bab')


class TestComMonoidAB:
    def test_equality_identity(self) -> None:
        assert ab_alg(AB('')) == ab_alg(AB(''))
        assert ab_alg(AB('')) is ab_alg(AB(''))
        assert ab_alg(AB('aabbbbaaab')) == ab_alg(AB('aaabaabbbb'))
        assert ab_alg(AB('aabbbbaaab')) is ab_alg(AB('aaabaabbbb'))

    def test_add(self) -> None:
        assert ab_alg(AB('')) + ab_alg(AB('')) == ab_alg(AB(''))
        assert ab_alg(AB('')) + ab_alg(AB('abab')) == ab_alg(AB('abab'))
        assert ab_alg(AB('baba')) + ab_alg(AB('')) == ab_alg(AB('bbbabbaaa'))
        assert ab_alg(AB('baaa')) + ab_alg(AB('aaabb')) == ab_alg(AB('bab'))
        assert ab_alg(AB('')) + ab_alg(AB('')) is ab_alg(AB(''))
        assert ab_alg(AB('')) + ab_alg(AB('abab')) is ab_alg(AB('abab'))
        assert ab_alg(AB('baba')) + ab_alg(AB('')) is ab_alg(AB('bbbabbaaa'))
        assert ab_alg(AB('baaa')) + ab_alg(AB('aaabb')) is ab_alg(AB('bab'))

    def test_mult_int(self) -> None:
        zero = ab_alg(AB(''))
        a = ab_alg(AB('a'))
        b = ab_alg(AB('b'))
        ab = ab_alg(AB('ab'))
        ba = ab_alg(AB('ba'))

        assert zero*0 == 0*zero == zero
        assert a*0 == 0*a == zero
        assert ab*0 == 0*ab == zero
        assert a*3 == 3*a == a

        assert a() == AB('a')
        assert (a + b)() == AB('ab')

        assert 5*(a + b) == 5*ab
        assert (3*a) + (b*2) == ab
        assert b + ab*2 == ba*2 + b + a + b + a + b
