__author__ = 'johannes'
from pony.orm import Database, sql_debug
DB = Database("postgres", host="localhost", user="johannes", password="break1Down", database="bike_rental")

class Singleton():
    singleton = None

    @staticmethod
    def get_instance():
        if not Singleton.singleton:
            Singleton.singleton = Singleton()
        return Singleton.singleton

    def __init__(self):
        self.current_user = None