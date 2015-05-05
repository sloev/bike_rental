__author__ = 'johannes'
from settings import DB
import npyscreen

import pony.orm as pny
from models import *

import auth
import logging
logging.basicConfig(filename='bike_rental.log', level=logging.INFO)
logging.info('Started')

class Singleton():
    singleton = None

    @staticmethod
    def get_instance():
        if not Singleton.singleton:
            Singleton.singleton = Singleton()
        return Singleton.singleton

    def __init__(self):
        self.current_user = None



class LoginForm(npyscreen.Form):
    def create(self):
        super(LoginForm, self).create()
        self.name = "Welcome to login screen"
                                              # I've ommitted it from later example code.
        self.username = self.add(npyscreen.TitleText, name='Username')
        self.password = self.add(npyscreen.TitlePassword, name='Password')

    def afterEditing(self):

        with pny.db_session:
            user = User.get(username=self.username.value)
            if user:
                if auth.authenticate(user.password, user.salt, self.password.value):
                    Singleton.get_instance().current_user = user

                    if isinstance(user, Admin):
                        self.parentApp.setNextForm('Admin')
                    elif isinstance(user, Customer):
                        self.parentApp.setNextForm('Customer')
                    elif isinstance(user, Manager):
                        self.parentApp.setNextForm('Manager')
                    elif isinstance(user, Mechanic):
                        self.parentApp.setNextForm('Mechanic')
                else:
                    self.parentApp.setNextForm(None)

class Profile(npyscreen.Form):
    def create(self):
        super(Profile, self).create()
        self.setup()

    def setup(self):
        self._profile_type = ""

    def beforeEditing(self):
        self.user = Singleton.get_instance().current_user
        self.name = "%s | %s" % (self._profile_type, self.user.first_name)

class CustomerProfile(Profile):
    def setup(self):
        self._profile_type = "Customer"

class ManagerProfile(Profile):
    def setup(self):
        self._profile_type = "Manager"

class AdminProfile(ManagerProfile):
    def setup(self):
        self._profile_type = "Admin"

class MechanicProfile(Profile):
    def setup(self):
        self._profile_type = "Mechanic"


class MyApplication(npyscreen.NPSAppManaged):
   def onStart(self):
       self.registerForm('MAIN', LoginForm())
       self.registerForm('Customer', CustomerProfile())
       self.registerForm('Admin', AdminProfile())
       self.registerForm('Manager', ManagerProfile())
       self.registerForm('Mechanic', MechanicProfile())

if __name__ == '__main__':
    TestApp = MyApplication().run()