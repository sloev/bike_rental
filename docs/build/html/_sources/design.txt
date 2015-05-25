Design
======

I started this project from the Python point of view. Which meant i focussed on how i would implement the application and secondary the application.

This proved early to be a wrong decision. Signs of this showed through my use of object relational mapping frameworks such as Pony ORM for python.
Nothing is wrong with Pony ORM if you want to degrade your database to secondary citizen in the system.
However since this class is about database design i wanted to focus on the development of a data centric system with lower priority on the implementation of the application layer.

In the start i had developed a schematic representation full of inheritance since i come from object oriented programming paradigms.

I wanted different roles for users in my system and wanted to be able to restrict actions based on these rules. Pony ORM gave me easy inheritance so i could implement a base user with details like password, username, address etc and then inherit from that user in my employee and customer. Admins, mechanics and managers would then inherit from the employee and so forth. Before long i recognized i needed to see which kind of tables Pony ORM were generating and i was horrorfied to see that it used table per hierachy inheritance.

As i said before inheritance is not a database concept in the normal sense. Postgresql has implemented inheritance but it lacks a lot of important functionality and is in general not recommended, they even have a disclaimer in their documentation telling of the faulty implementation [#postgresql_inheritance]_.

In normal sql you implement inheritance by going with one of two popular concepts:

* Table per hierachy
* Table per type
  

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


.. [#sql_antipatterns] https://pragprog.com/book/bksqla/sql-antipatterns



.. [#postgresql_inheritance]  ndosn