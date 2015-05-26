Normalization
=============

I have normalized the database to a certain extend. I have not gone into the extremes where you reach nearly a "singleton"-ness of all data.

Noprmalization is when you seek to reduce redundancy in your database and try to design it without a certain functionality in mind but instead with focus on the stored data and the ability to query this freely.

First normal form
'''''''''''''''''
I have been carefull to design the database so redundancy in table rows are avoided. 
Furthermore i am using unique identifiers for all tables except those where their attributes are directly coupled to other tables through their primary key being a foreign key.

Second normal form
''''''''''''''''''

I have spread out the data and produced primary keys that through foreign keys link together the bits of information that are assoociated.

For example the users are a diverse entity. All users share basic data however their responsibilities and specialities are very diverse. I made sure to include only the necersary information in the base user, and whenever i found attributes which could be shared by many users or other entities i forked it into its own table and left a foreign key pointing to it, the users are pointing to an address row for example.

Another example is that i am using *type* id's in both the user and contract tables to identify which other table i should look in to find more info.
This is very flexible since i can add more contract types and more types of users without modifying the *User* table or the *Contract* table. Only the queries would have to be manipulated with extra *joins*.


Third normal form
'''''''''''''''''

My project is implementing the third normal form by keeping redundancies at minimum. However the project has not gone all the way.

In the current design i have not normalized areas such as:

user.first_name / user.last_name 
	These info could be spread into each their own tables like i have done with the details.phone.

However i have succesfully normalized the *contracts* for example.
Contracts are defined by a *contract_id*. This id is the foreign key for a lot of attributic tables that all have the ability of adding more data to the context of a contract.

The *contracts.bill* is a unique item. Its fields are sparse and specific for each instance. Only one bill can exist for each contract but a bill can be associated with any given *Type* of contract. therefor the bill is not an attribute of the contract but more an attribute you can associate with a contract_type like the *rental_contract*. The *rental_contract* needs a bill because the rental contract involves outbound busines. The *repair contract* on the other hand is inbound and relies on the mechanic who allready receives a paycheck.

Redundancy is minimal in this setup and tables are only populated if they are needed to.
The only downside is the rather complex queries and inserts when you are working with these *splitted out* tables.

.. raw:: pdf

   PageBreak