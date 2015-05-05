__author__ = 'johannes'

from settings import DB
import pony.orm as ponyorm
#sfrom models import *
print DB.generate_mapping(create_tables=True)
def a():
    DB.drop_table("Bill", if_exists=True, with_all_data=True)
    #DB.drop_all_tables(with_all_data=True)
    #DB._drop_tables(*["Address"],if_exists=True,with_all_data=True)
    DB.commit()

a()