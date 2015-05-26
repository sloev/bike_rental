Implementation
==============

I will here go through the different tables with a focus on the most complex functionality.
All examples depend on the execution of the *appendice/test script*.

Please see the the *appendice/setup script* for a complete walkthrough of the creation of all tables, schemas and functions.

Users
-----

The *user* table holds all attributes held by all users. The attributes hold personal data such as contact information as well as system critical data such as usernames and passwords.

The *user* table hold three foreign keys:

**address_id**
	An int pointing to an address record
**phone_id**
	An int pointing to a phone number
**type**
	An int pointing to a *users.type* record

The *type* attribute is special since it acts as a descriminator in the application layer.
The application layer will descriminate different functionalities based on which user type you pocess.

Security
''''''''

I wanted a secure way of logging in so i implemented password hashing so the database only stores hashed passwords.
When you hash passwords you use a random salt to make a hash digest of a clear text password. The output password is regarded as inreversable and secure however you have to store the random salt in order to verify future clear text passwords against the stored password hash.

If the connection to the database is secure, then my implementation is also secure or at least standard.

The diagram below describes the process where the application layer is:

* Creating a user
* Updating the user with a hashed password
* Authenticating the user through the database with a clear text password.

.. figure:: /images/login_seq.png
   :figwidth: 90%
   :scale: 200%

   Diagram shows the creation of user, the updating of a user's password and the authentication of a user.

.. comment
   .. seqdiag::
      seqdiag {
      application => postgresql [label = "all data regarding a user was entered to the system"];
      === Change password ===
      application -> postgresql [label = "select * from\nfunctions.update_login('admin', 
      '1234'"];
      postgresql -> postgresql [label = "python:\ngenerate salt\n\ncompute hash from password and salt\n\nstore hash and salt"]
      application <- postgresql [label = "OK"];
      === Log in ===
      application -> postgresql [label = "select * from\nfunctions.login('admin', '1234'"];
      postgresql -> postgresql [label = "python:\nquery user\n\ncompute password from stored salt and given password\n\ncompare stored password with computed password"]
      application <- postgresql [label = "response = all details on user"];
      }

I chose to implement the above functionality in python and use the python procedural language for postgresql for execution.
I wanted the functionality as a stored procedure so it didn't affect my database design.

If i wanted a function to return a predecided set of attributes i needed a custom type. Postgresqls PL lets you return composite attributes only if you have defined a *"holder"* type for these. The following *login_type* was developed for the *login* function.

.. literalinclude:: sql/setup.sql
   :language: sql
   :linenos:
   :lines: 115-131

I developed an authentication python module with the needed functions for creating hashes and so forth. But i did not install it system wide so my two sotred procedures, *login* and *update_login*, each have it embedded in their source.
I have omitted these parts and instead left a print of the python module in the *appendice/hashing*.

Login
.....

Applications use the *login* PL function when logging in. The *login* function uses python as language and depends on a few python modules for hashing and digesting.

.. literalinclude:: sql/setup.sql
   :language: python
   :linenos:
   :lines: 135-137, 163-208

As you see this is not straight python, a few extras are assumed existing as you type. These extras are given at runtime by the postgresql python PL extension. 

Amongst these are the *SD* dictionary which is a global dictionary offered to handle sharing of data between python scripts. But more interesting is the *plpy* object which is the gateway to execute queries from within the python script. I am using the *plpy* object both in the *login* and *update_login* functions.

Example
,,,,,,,

The *login* function is used through a select query. 
This example depends on the existence of an *admin* user with the username *"admin"* and the password *"1234"*.
The *login* function will return the fully populated *login_type* if succesfull or a list of null values of similar length.

.. code-block:: sql
   
   select * from functions.login('admin', '1234');

The query will yield the following resultset:

.. figure:: images/login_sql.png
   :figwidth: 100%


Update_login
............


An application can update a users password only by also generating a new salt and using this to hash the given clear text password.

Applications use the *update_login* function in two scenarios:

1. When creating a user the first step involves creating a user, the second updating the user with a password/salt.
2. When a user wants to alter its password, think *"forgotten password"* functionality.

The *update_login* function uses the *plpy* object for updating a *user* record with a new hashed password/salt pair.

.. literalinclude:: sql/setup.sql
   :language: python
   :linenos:
   :lines: 210-212, 237-249

Example
,,,,,,,

This example will generate take the new password, generate a random salt and hash the given password.
This new hashed password will be stored and if all goes well an *"OK"* response will be returned as text.

.. code-block:: sql
   
   select * from functions.update_login('admin', '5678');

The query yields the following result:

.. figure:: images/update_login_sql.png
   :figwidth: 30%

Contracts
---------

Contracts are the business in this project. The contracts tell about which bikes are occupied at any given time, they are responsible for billing and they are also used when the bikes are in need of repair.

The contracts are designed as a base contract  table and a type table.
The base contract table, *contracts.contract*, only hold universal information such as begin and end date of the contract, which bike it involves and a foreign key pointing to a contract type.

The *contracts.contract_type* is used for telling the application code which other tables to join when querying for all data regarding a contract.

Example
'''''''

For example if you want to query a specific rental contract you might do the following:

.. code-block:: sql

   select * from contracts.contract c where c.contract_id = 1

Will yield

.. figure:: images/contract_1.png
   :figwidth: 100%
   :scale: 300%

This result tells us that the contract is a *rental_contract* but it does include the *rental_contract* specific attributes in its result set.

The test script creates two kinds of contracts *rental* and *repair* if we include these in our query we will receive resultset including attribute from both tables if existing. Furthermore we also get a contract_type collumn with the descriptive name instead of the *type_id*.
Modified to show all contracts and all contract attributes it looks like this:

.. literalinclude:: sql/contract_query.sql
   :language: sql
   :linenos:

This yields the complete data set of a contract including id's of customers if its a rental contract or the assigned employee if its a repair contract.

.. figure:: images/contract_2.png
   :figwidth: 100%
   :scale: 300%


The result is a denormalized resultset filled with nulls where rows are missing in the involved tables. As expected only attributes regarding the contract type exists in each row.


Bikes
-----

Bikes are the product. They are the unique combination of a bike type and a serial number. A special collumn hold all information regarding the bike type. Like description and color.
Bikes are also the subject of reports. Reports can be everything from a report on what was fixed during the repair of a bike, to the planning of bike modificatins etc.

Example
'''''''

Bikes can be queried in a similar fashion as the other entities. and if you want to include the attributes from the bike type table you can use the following query:

.. literalinclude:: sql/bike_query.sql
   :language: sql
   :linenos:

Which yields the following result set:

.. figure:: images/bike_1.png
   :figwidth: 100%
   :scale: 300%




If you want to query which reports there is on a bike you can use the following query:

.. code-block:: sql

   SELECT *
   FROM contracts.report report
   WHERE report.serial_number = 1122134;

Which yields the following resultset:

.. figure:: images/bike_2.png
   :figwidth: 100%
   :scale: 300%




.. raw:: pdf

   PageBreak



