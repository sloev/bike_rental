__author__ = 'johannes'
from settings import DB, Singleton
import npyscreen

import pony.orm as pny
from models import *

import auth
import logging
logging.basicConfig(filename='bike_rental.log', level=logging.INFO)
logging.info('Started')


class LoginForm(npyscreen.Form):
    def create(self):
        super(LoginForm, self).create()
        self.name = "Welcome to login screen"
                                              # I've ommitted it from later example code.
        self.username = self.add(npyscreen.TitleText, name='Username')
        self.password = self.add(npyscreen.TitlePassword, name='Password')

    def beforeEditing(self):
        self.username.value = ""
        self.password.value = ""

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
        self.log_out_button = self.add(npyscreen.ButtonPress, name="log out!")
        self.log_out_button.whenPressed = self._logout
        self.setup()

    def _logout(self):
        self.parentApp.setNextForm("MAIN")
        self.exit_editing()

    def setup(self):
        self._profile_type = ""

    def beforeEditing(self):
        self.user = Singleton.get_instance().current_user
        self.name = "[ %s ]  -  logged in as: \"%s\"" % (self._profile_type, self.user.username)

class CustomerProfile(Profile):
    def setup(self):
        self._profile_type = "Customer"

class EmployerProfile(Profile):
    def create(self):
        super(EmployerProfile, self).create()

        self.list_repair_contracts_button = self.add(npyscreen.ButtonPress, name="List repair contracts")
        self.list_repair_contracts_button.whenPressed = self._list_repair_contracts

    def _list_repair_contracts(self):
        pass

class ManagerProfile(EmployerProfile):
    def setup(self):
        self._profile_type = "Manager"

class AdminProfile(ManagerProfile):
    def setup(self):
        self._profile_type = "Admin"

class MechanicProfile(EmployerProfile):
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