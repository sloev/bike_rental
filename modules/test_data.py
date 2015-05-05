__author__ = 'johannes'
from settings import DB

from models import *
import pony.orm as ponyorm
from pony.orm import Database, sql_debug
from datetime import datetime


from random import randint


@ponyorm.db_session
def create_users(amount):
    customer_id = 0
    first_names = ["jens", "paul", "kurt", "pia", "anders"]
    last_names = ["andersen", "holgersen", "tolstoj", "pontopidan"]
    street_names = ["frigade", "vestergade", "frimestervej", "bredgade", "nordefasanvej"]
    cities = ["nyborg", "aalborg", "svendborg", "ringsted"]
    username = "username_"
    password = "1234"
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

        _username = "%s%d" %(username, i)

        customer = Customer(username=_username, password=password, user_id=customer_id, first_name=first_name, last_name=last_name, address=address, phone=phone, creation_date=datetime.now())
        cus = customer
    cus.is_admin = True

if __name__ == "__main__":
    sql_debug(True)
    print DB.generate_mapping(create_tables=True)
    create_users(10)
    DB.commit()