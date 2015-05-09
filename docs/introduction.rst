============
Introduction
============

This report will describe the the creation of a database system for a bike rental company called "Wheels".
"Wheels" is a company renting out bikes and its staff includes managers that take care of customers and mechanics
that take care of bikes.

Problem formulation
-------------------
The bike rental company "Wheels" wants an application to manage and hold data on their employees, customers and bikes.
They want a system where customers and employees can login and where managers can create rental contracts with customers.
The system shall hold basic information on all its users like address, phonenumber, name etc and all users will have their
own user-id. Furthermore the system should give special privileges according to the whether the user is a customer,
mechanic, manager or admin. They only want admins to be able to create new employees, but managers should be able to
create new customers. Mechanics should be responsible of receiving bikes from customers create repair contracts on them so
their condition can be monitored. The system should detect if a bike is rented out and only offer bikes for rent that are
not currently rented out.
Each bike should have its unique serial number as well as details on type of bike stored in the system.

Requirements
------------

+-------+------------------------------------------------------------------------------+
| Name  |Description                                                                   |
+=======+==============================================================================+
|R1     |Information bikes must be stored in the system, such as serial number, color, |
|       |description etc.                                                              |
+-------+------------------------------------------------------------------------------+
|R2     |Information on all users should be stored in the system such as name, sir-name|
|       |username, password, address etc.                                              |
+-------+------------------------------------------------------------------------------+
|R3     |Passwords has to be hashed with a random salt before saved and both salt and  |
|       |hashed password will be saved.                                                |
+-------+------------------------------------------------------------------------------+
|R4     |Three types of employees must exist and all must inherit from the abstract    |
|       |employee who again inherits from user. The kinds of employees are: manager,   |
|       |admin and mechanic                                                            |
+-------+------------------------------------------------------------------------------+
|R5     |Contracts must be saved in the database and must include dates of start and   |
|       |end. The rental contracts must include information on whether they are paid   |
|       |and which customer they are associated to. Repair contracts must include      |
|       |information on which mechanic they are attached to as well as space for an    |
|       |optional repair report. Both must have fields to tell if they have been       |
|       |fulfilled                                                                     |
+-------+------------------------------------------------------------------------------+
|R6     |A commandline application must be created implementing the system features    |
+-------+------------------------------------------------------------------------------+
|R7     |Users should only be able to view and edit their own contracts                |
+-------+------------------------------------------------------------------------------+