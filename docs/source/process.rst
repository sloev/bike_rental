Process
=======

I started out with a different project that ended up taking nearly all mty time until i recognized its lack of importance in regards to database aspects. See more on this in the *appendice/proposed projects*

After i terminated the old project i decided to implement the classic rental system but with a twist being a bike rental instead of cars.

ORM's
-----

I made the mistake to focus on the development of an application and secondarily the database which led me to the use of different Object Relational Mapping libraries like Pony ORM.

ORM's give you the ability to treat the database as a second class citizen and focus on the business logic however when i saw which kind of sql the Pony ORM propuced i was convinced i went in a wrong direction.

Early on i had established a sketch of the overall system with different kinds of users, contracts and bikes and their relations but the ORM gave me the ability to create inheritance.

Pony ORM used table per hierachy inheritace where it would store all attributes for all different subclasses in the same table. A special *"class type"* attribute would then be used in the application layer to discriminate which attributes a query would produce.
This kind of inheritance produces a lot of unpopulated cells in the database and it lowers the speed of query significantly.

I relized i had implemented a sql-antipattern by producing my database with a focus on being object-oriented. 

Database in focus
-----------------

After skipping the ORM's and diving straight for sql i also lost the rapid development in the process.
I decided to focus on implementing the sql and developing the needed queries for an eventual application layer.
I wanted to use the Stored Procedures and the Python extension to develop complex functions that would replace a lot of the heavy business logic in the application layer.
In this way i could present a solution that would in precise words tell how to implement the application logic without having it as the main focus.

.. raw:: pdf

   PageBreak