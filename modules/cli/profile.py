__author__ = 'johannes'
"""profile

this module does a lot of things, you can use multilines and double newlines creates sections

Attributes:
  module_level_variable (int): description of variable
"""
import npyscreen
from settings import *

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
        self.create_new_employee_button = self.add(npyscreen.ButtonPress, name="Create employee!")
        self.create_new_employee_button.whenPressed = self._new_employee

    def _new_employee(self):
        self.parentApp.setNextForm("NewEmployee")
        self.exit_editing()


class MechanicProfile(EmployerProfile):
    def setup(self):
        self._profile_type = "Mechanic"