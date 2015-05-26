Appendices
==========

Vocabulary
----------

PL
	Precedural Language
Python
	Object orinted programming language
Plpython 
	An extension to postgresql that lets you write python inside PL functions
Plpy
	The object from which you can query the database from PLPython

Hashing
-------
The following hashing functionality was implemented in python as a module.
*_* is used as a descriptor for private, *internal*, functions.

.. literalinclude:: python/auth.py
   :language: python
   :linenos:

Proposed projects
-----------------

In the beginning i wanted to extend a project i had been working on for a year called *"the obama puppet"*.  
The project was a database system where a application would analyse president Obama's weekly addresses and cut every word out as a video sample. These samples would then be saved in a postgresql database and a Procedural Language function would be able to generate a new video from a query based on the stored samples.

I went through with the project but realized too late that it didn't involve enough interesting aspects regarding the database. I set the project on pause for a day and evaluated which features could extend it into a full database project and realized it would be more work than starting a new project instead.

The *"obama puppet"* was terminated right after i had implemented a twitter bot for it, allowing everybody to let him speak their speeches.

It can be found at:
http://github.com/sloev/obama-puppet

Inheritance in sql
------------------

In general two kinds of inheritance exist in sql. Each have their downsides but both are generally seen as antipatterns where you develop the database from an object oriented paradigm instead of a relational database system paradigm.

Table Per Hierarchy Inheritance
'''''''''''''''''''''''''''''''

You implement all attributes of all children in a single table with an extra attribute telling the kind of child.

Requires the application to implement logic that creates a meta layer over the existing table. This meta layer will differentiate the
table into virtual sub tables, and know which attributes belong to which subclasses. This is not trivial.
Might suffer in speed if there is not equality between the quantity of the children.

For example if parent a hast 10 children, where 9 of them are of type b and one of them is of type a. Then in worst case you could say that
the database would have to go through one miss before finding 9 hits if searching for type b, which is regarded as fast.
But it would have to go through 9 miss before finding 1 hit if searching for type a, which is awful.

Since the table must have all attributes for all sub classes it cant have required attributes that are not shared by all children.
This leaves a lot of validation to the application.

Creation/deletion of new types of subclasses would require mangling with the whole table including and potentially
adding/removing attributes from all instances of all subclasses.

Table Per Type Inheritance
''''''''''''''''''''''''''

Or you create an abstract parent implementing all common attributes of its children and then create a specific table for
each kind of child with a reference to its parent.
You could have an abstract employee table that held all information shared by employees like salary, employer-id etc.
And then create a new table pr type of child all having a reference to a unique row in the parent.

Requires the application to join data from multiple tables pr query. One join pr level of inheritance at the least. This is a trivial task but reduces speed pr query.

Setup script
------------

The following script is used to construct all tables, functions, schemas etc for the system.

.. literalinclude:: sql/setup.sql
   :language: sql
   :linenos:

Drop script
-----------

This script is used to drop all related to this project.

.. literalinclude:: sql/drop.sql
   :language: sql
   :linenos:

Test script
-----------

All examples in this project are based on the following *test.sql* sql script. When run it will insert:

* Some addresses
* Some phone numbers
* A shop
* 4 users: customer, manager, mechanic, admin
  
.. literalinclude:: /sql/test.sql
   :language: sql
   :linenos:


