algebras
========

.. admonition:: Abstract Algebras Representations 
    
    Infrastructure for implementing concrete representations for
    abstract algebras of various types.

Protocols
---------

.. autoclass:: boring_math.abstract_algebra.algebras.NaturalMapping
    :exclude-members: __init__

Abstract Base Classes
---------------------

.. autoclass:: boring_math.abstract_algebra.algebras.BaseSet

.. autoclass:: boring_math.abstract_algebra.algebras.BaseElement
    :exclude-members: __add__, __mul__, __pow__, __neg__, __sub__, __truediv__

.. toctree::
    :caption: algebra modules

    semigroup
    monoid
    group
    commutative_semigroup
    commutative_monoid
    abelian_group
    ring
    commutative_ring
    field
