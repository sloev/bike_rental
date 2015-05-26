Conclusion
==========

I am very happy with the resulting database design and i find it very robust and future proof. I am happy that i went through so many iteraions ending up where i did because i learned a better more clean database design that way.

I sacrified the development of an application because time was running out and i had to choose between good database design and a good application.

I think i could have planned my process much better if i had given the requirements some extra thoughts in the beginning of the semester. 

Product and Process comments
----------------------------

I have used Sphinx and RestructuredText to write this report which made it possible to reduce the dificulties of writing since i was generating the layout on the fly. An added benefit was the live-reload preview of the report in a browser while i wrote the content in clear text. See http://sphinx-doc.org for more info.

Sourcecode for this project has been released as opensource on github at the following address:

http://github.com/sloev/bike_rental

And a html edition of this report is accessed via:

http://sloev.github.io/bike_rental

Requirements conclusion
-----------------------

**R1**
Is fulfilled by the *bikes* schema and its tables.

**R2**

Is fulfilled by the combination of the *users.user* table and the *details* schema and its tables.

**R3**

Is fulfilled by the two python PL functions *login* and *update_login*.

**R4**

This is not directlym implemented since i have learned that inheritance is not a good SQL design. Instead they are implemented as user types together with the customer. Each can of course have their own special table for extra attributes.

**R5**

Partly fulfilled as the *repair_contract* does not contain information on whether it has been completd. However the rest of R5 is fulfilled by the *contracts* schema, its tables and the collaborating tables from *bikes* etc.

**R6**

Is not fulfilled since i too late learned that an ORM would conceil bad SQL from me, so instead i focussed on the creation of a good database design with a few helping functions to ease the development of an application. For example all logging in has been taken care of by the database.

**R7**

Not implemented because of two things:

* I have not implemented an application to handle permissions etc.
* I have not instead implemented SQL roles and access control permissions for individual users.

.. raw:: pdf

   PageBreak