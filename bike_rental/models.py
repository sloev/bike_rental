__author__ = 'johannes'

from datetime import datetime
from decimal import Decimal

from pony.orm import PrimaryKey,Required,Set, Optional, sql_debug

from bike_rental.settings import DB as db


class Address(db.Entity):
    address_id = PrimaryKey(int, auto=True)
    street_name = Required(str)
    street_number = Required(int)
    zip = Required(int)
    city = Required(str)
    users = Set("User")


class Bike(db.Entity):
    bike_type = Required("Bike_type")
    contracts = Set("Contract")
    serial_number = PrimaryKey(int)


class Phone(db.Entity):
    number = PrimaryKey(str)
    user = Optional("User")


class User(db.Entity):
    first_name = Required(unicode)
    last_name = Required(unicode)
    phone = Optional(Phone)
    user_id = PrimaryKey(int, auto=True)
    creation_date = Required(datetime)
    username = Required(str, unique=True)
    password = Required(str)
    salt = Required(str)
    customer = Optional("Customer")
    employee = Optional("Employee")
    address = Required(Address)


class Customer(db.Entity):
    rental_contracts = Set("Rental_contract")
    user = Required(User)
    Customer_id = PrimaryKey(int, auto=True)


class Employee(db.Entity):
    salary = Optional(int)
    Employer_id = PrimaryKey(int, auto=True)
    user = Required(User)


class Manager(db.Employee):
    contracts = Set("Contract")


class Mechanic(db.Employee):
    repair_contracts = Set("Repair_contract")


class Contract(db.Entity):
    contract_id = PrimaryKey(int, auto=True)
    begin_date = Required(datetime)
    end_date = Required(datetime)
    manager = Required(Manager)
    bike = Required(Bike)


class Bike_type(db.Entity):
    bike_type_id = PrimaryKey(int, auto=True)
    name = Required(str, unique=True)
    weight = Optional(int)
    bikes = Set(Bike)
    color = Optional(str, nullable=True)
    description = Required(str)


class Rental_contract(db.Contract):
    customer = Required(Customer)
    bill = Optional("Bill")


class Repair_contract(db.Contract):
    mechanic = Optional(Mechanic)
    repair_report = Optional("Repair_report")
    done = Required(bool, default=False)


class Bill(db.Entity):
    paid = Required(bool, default=False)
    amount = Required(Decimal)
    rental_contract = PrimaryKey(Rental_contract)
    pay_date = Required(datetime)


class Repair_report(db.Entity):
    repair_contract = PrimaryKey(Repair_contract)
    report_text = Required(str)


class Admin(db.Manager):
    pass


sql_debug(True)
print db.generate_mapping(create_tables=True)