__author__ = 'johannes'

from datetime import datetime
from decimal import Decimal
from pony.orm import PrimaryKey,Required,Set, Optional

from app import DB as db

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


class Customer(db.User):
    rental_contracts = Set("Rental_contract")


class Employer(db.User):
    salary = Optional(int)


class Manager(db.Employer):
    contracts = Set("Contract")


class Mechanic(db.Employer):
    repair_contracts = Set("Repair_contract")


class Contract(db.Entity):
    contract_id = PrimaryKey(int, auto=True)
    begin_date = Required(datetime)
    end_date = Required(datetime)
    bike = Required(Bike)
    manager = Required(Manager)


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


class Rental_contract(db.Contract):
    customer = Required(Customer)
    bill = Required("Bill")


class Repair_contract(db.Contract):
    mechanic = Optional(Mechanic)
    repair_report = Optional("Repair_report")
    done = Required(bool, default=False)


class Bill(db.Entity):
    bill_id = PrimaryKey(int, auto=True)
    paid = Required(bool, default=False)
    amount = Required(Decimal)
    rental_contract = Optional(Rental_contract)
    pay_date = Required(datetime)


class Repair_report(db.Entity):
    repair_report_id = PrimaryKey(int, auto=True)
    repair_contract = Required(Repair_contract)
