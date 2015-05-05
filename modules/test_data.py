__author__ = 'johannes'

from settings import DB

from models import *
import pony.orm as ponyorm
from pony.orm import Database, sql_debug
from datetime import datetime


from random import randint
import auth

@ponyorm.db_session
def create_users(amount):
    customer_id = 0
    first_names = ["jens", "paul", "kurt", "pia", "anders"]
    last_names = ["andersen", "holgersen", "tolstoj", "pontopidan"]
    street_names = ["frigade", "vestergade", "frimestervej", "bredgade", "nordefasanvej"]
    cities = ["nyborg", "aalborg", "svendborg", "ringsted"]
    username = "username_"
    _password = "1234"
    cus = None
    for i in range(amount):
        customer_id+=1
        phone_number_string = "%08d" % randint(0,99999999)
        phone = Phone(number=phone_number_string)

        street_name = street_names[randint(0,len(street_names)-1)]
        city = cities[randint(0,len(cities)-1)]
        address = Address(street_name=street_name, street_number=randint(0,400), zip=randint(1000,9999), city=city)

        first_name = first_names[randint(0,len(first_names)-1)]
        last_name = last_names[randint(0,len(last_names)-1)]

        salt, password = auth.create_password_from_clear(_password)

        _username = "%s%d" %(username, i)

        customer = Customer(username=_username,salt=salt, password=password, first_name=first_name, last_name=last_name, address=address, phone=phone, creation_date=datetime.now())
    address = Address(street_name="gade", street_number=randint(0,400), zip=randint(1000,9999), city="svendborg")
    phone = Phone(number="60805762")
    salt, password = auth.create_password_from_clear(_password)

    admin = Admin(username="admin", salt=salt, password=password, first_name="cavin", last_name="hobbs", address=address, phone=phone, creation_date=datetime.now())

if __name__ == "__main__":
    create_users(10)
    DB.commit()