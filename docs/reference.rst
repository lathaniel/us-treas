API Reference
=============

Classes
-------

.. autoclass:: ustreas.rates.Rate
   :members:

.. autoclass:: ustreas.rates.YieldCurve
   :members:
   :show-inheritance:

.. autoclass:: ustreas.rates.Bill
   :members:
   :show-inheritance:

.. autoclass:: ustreas.rates.LongTerm
   :members:
   :show-inheritance:

Usage & Examples
----------------

Example 1: Getting Yield Curve data

.. code:: python

  import ustreas as treas

  x = treas.YieldCurve()

  hist = x.history()

  hist.to_csv('path/to/file.csv', index = False)