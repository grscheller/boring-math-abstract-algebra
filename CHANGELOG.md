# CHANGELOG

PyPI pythonic-fp-protocols project.

## Semantic Versioning

Strict 3 digit semantic versioning.

- **MAJOR** version incremented for incompatible API changes
- **MINOR** version incremented for backward compatible added functionality
- **PATCH** version incremented for backward compatible bug fixes

See [Semantic Versioning 2.0.0](https://semver.org).

## Releases and Important Milestones

### Update - 2025-11-07

- elements
  - elements know the concrete algebra to which they belong
  - they wrap hashable immutable representations
  - binary operations * and + act on the elements
    - not their representations
- algebras
  - contain an dict of their potential elements
    - can be used with potentially infinite or continuous algebras
    - the dict is "quasi-immutable"
      - elements are added in a "natural" unique deterministic way
  - contain user defined methods that take representations as parameters
  - contain attributes like
    - a monoid identity element
    - a ring's additive and multiplicative identities

### Update - 2025-10-17

Major increase in my understanding of Protocols.

- decided to move project to Boring Math
- renaming repo pythonic-fp-protocols -> boring-math-abstract-algebra

### Update - 2025-10-13

Narrowing scope of project to just protocols.

- renaming repo to pythonic-fp-protocols
- began work on module pythonic-fp-protocols.algebraic

### Created  - 2025-10-12

Created GitHub repo pythonic-fp-typing for a future PyPI project of that
name.
