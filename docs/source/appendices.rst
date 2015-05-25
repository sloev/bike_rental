Appendices
==========


Hashing
-------
The following hashing functionality was implemented in python as a module.
*_* is used as a descriptor for private, *internal*, functions.

.. literalinclude:: login.py
   :language: python
   :linenos:
   :lines: 150-

Test data
---------

All examples in this project are based on the following *test.sql* sql script. When run it will insert:

* Some addresses
* Some phone numbers
* A shop
* 4 users, on of each kind
  
.. literalinclude:: /sql/test.sql
   :language: sql
   :linenos:
