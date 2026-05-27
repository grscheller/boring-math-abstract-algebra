Usage
=====

How to installing the package
-----------------------------

Install the project into your Python environment:

.. code:: console

    $ pip install boring-math-abstract-algebra

Importing the modules
---------------------

Import classes needed to define your own algebras.

.. code:: python

    from boring_math.abstract_algebra.semigroup import Semigroup
    from boring_math.abstract_algebra.monoid import Monoid
    from boring_math.abstract_algebra.group import Group
    from boring_math.abstract_algebra.commutative_semigroup import CommutativeSemigroup
    from boring_math.abstract_algebra.commutative_monoid import CommutativeMonoid
    from boring_math.abstract_algebra.abelian_group import AbelianGroup
    from boring_math.abstract_algebra.ring import Ring
    from boring_math.abstract_algebra.commutative_ring import CommutativeRing
    from boring_math.abstract_algebra.field import Field

Algebra class hierarchy
-----------------------

Arrows point from super class to sub classes. Class BaseSet is abstract.

.. graphviz::

    digraph Modules {
        bgcolor="#957fb8";
        node [style=filled, fillcolor="#181616", fontcolor="#dcd7ba"];
        edge [color="#181616", fontcolor="#dcd7ba"];
        CommutativeMonoid -> AbelianGroup;
        CommutativeSemigroup -> CommutativeMonoid;
        "BaseSet (Abstract)" -> CommutativeSemigroup;
        Ring -> CommutativeRing;
        CommutativeRing -> Field;
        Monoid -> Group;
        Semigroup -> Monoid;
        AbelianGroup -> Ring;
        "BaseSet (Abstract)" -> Semigroup;
    }
