__author__ = 'johannes'
from pony.orm import Database, sql_debug
DB = Database("postgres", host="localhost", user="johannes", password="break1Down", database="bike_rental")
