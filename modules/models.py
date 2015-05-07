__author__ = 'johannes'

from datetime import datetime
from decimal import Decimal
from pony.orm import PrimaryKey,Required,Set, Optional, sql_debug

from settings import DB as db



class Address(db.Entity):
    address_id = PrimaryKey(int, auto=True)
    street_name = Required(str)
    street_number = Required(int)
    zip = Required(int)
    city = Required(str)
    user = Optional("User")


class Bike(db.Entity):
    bike_type = Required("Bike_type")
    bike_serial = PrimaryKey("Bike_serial")
    contracts = Set("Contract")


class Phone(db.Entity):
    number = PrimaryKey(str)
    user = Optional("User")


class User(db.Entity):
    first_name = Required(unicode)
    last_name = Required(unicode)
    address = Required(Address)
    phone = Optional(Phone)
    user_id = PrimaryKey(int, auto=True)
    creation_date = Required(datetime)
    username = Required(str, unique=True)
    password = Required(str)
    salt = Required(str)
    customer = Optional("Customer")
    employee = Optional("Employee")


class Customer(db.Entity):
    rental_contracts = Set("Rental_contract")
    user = Required(User)
    Customer_id = PrimaryKey(int, auto=True)


class Employee(db.Entity):
    salary = Optional(int)
    Employer_id = PrimaryKey(int, auto=True)
    user = Required(User)
    manager = Optional("Manager")
    mechanic = Optional("Mechanic")


class Manager(db.Entity):
    contracts = Set("Contract")
    employee = Required(Employee)
    admin = Optional("Admin")


class Mechanic(db.Entity):
    repair_contracts = Set("Repair_contract")
    employee = Required(Employee)


class Contract(db.Entity):
    contract_id = PrimaryKey(int, auto=True)
    begin_date = Required(datetime)
    end_date = Required(datetime)
    bike = Required(Bike)
    manager = Required(Manager)
    rental_contract = Optional("Rental_contract")
    repair_contract = Optional("Repair_contract")


class Bike_type(db.Entity):
    bike_type_id = PrimaryKey(int, auto=True)
    name = Required(str, unique=True)
    weight = Optional(int)
    bikes = Set(Bike)
    color = Optional(str, nullable=True)
    description = Required(str)


class Bike_serial(db.Entity):
    bike = Optional(Bike)
    serial_number = PrimaryKey(int)


class Rental_contract(db.Entity):
    customer = Required(Customer)
    bill = Required("Bill")
    contract = Required(Contract)


class Repair_contract(db.Entity):
    mechanic = Optional(Mechanic)
    repair_report = Optional("Repair_report")
    done = Required(bool, default=False)
    contract = Required(Contract)


class Bill(db.Entity):
    bill_id = PrimaryKey(int, auto=True)
    paid = Required(bool, default=False)
    amount = Required(Decimal)
    rental_contract = Optional(Rental_contract)
    pay_date = Required(datetime)


class Repair_report(db.Entity):
    repair_report_id = PrimaryKey(int, auto=True)
    repair_contract = Required(Repair_contract)


class Admin(db.Entity):
    manager = Required(Manager)


sql_debug(True)
print db.generate_mapping(create_tables=True)