__author__ = 'johannes'
"""login

this module does a lot of things, you can use multilines and double newlines creates sections

Attributes:
  module_level_variable (int): description of variable
"""

import npyscreen

from settings import *
from models import User, Admin, Mechanic, Manager, Address, Phone
from datetime import datetime
import auth

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
                    if user.employee:
                        if isinstance(user.employee, Admin):
                            self.parentApp.setNextForm('Admin')
                        elif isinstance(user.employee, Manager):
                            self.parentApp.setNextForm('Manager')
                        elif isinstance(user.employee, Mechanic):
                            self.parentApp.setNextForm('Mechanic')
                    elif user.customer:
                        self.parentApp.setNextForm('Customer')
                    else:
                        self.parentApp.setNextForm(None)
                else:
                    self.parentApp.setNextForm(None)


class NewAccountForm(npyscreen.ActionForm):
    def create(self):
        super(NewAccountForm, self).create()
        self.username = self.add(npyscreen.TitleText, name='Username')
        #self.password = self.add(npyscreen.TitlePassword, name='Password')
        #all new passwords are 1234
        self.first_name = self.add(npyscreen.TitleText, name='First name')
        self.last_name = self.add(npyscreen.TitleText, name='Last name')
        self.street_name = self.add(npyscreen.TitleText, name='Street name')
        self.street_number = self.add(npyscreen.TitleText, name='Street number')
        self.zip_code =self.add(npyscreen.TitleText, name='Zip code')
        self.city = self.add(npyscreen.TitleText, name='City')
        self.phone = self.add(npyscreen.TitleText, name='Phone number')
        self.salary = self.add(npyscreen.TitleText, name='[optional] Salary')
        self.employee_type = self.add(npyscreen.TitleSelectOne, max_height=4, value = [1,], name="Employee type",
                values = ["Manager","Admin","Mechanic"], scroll_exit=True)
        self.setup()

    def setup(self):
        pass

    def beforeEditing(self):
        pass

    @pny.db_session
    def on_ok(self):
        address = Address(street_name=self.street_name.value, street_number=int(self.street_number.value), zip=int(self.zip_code.value), city=self.city.value)
        phone = Phone(number=self.phone.value)

        salt, password = auth.create_password_from_clear("1234")
        user = User(username=self.username.value,
                salt=salt,
                password=password,
                first_name=self.first_name.value,
                last_name=self.last_name.value,
                address=address,
                phone=phone,
                creation_date=datetime.now())
        address.user=user
        phone.user=user
        self._after_editing(user)
        DB.commit()
        self.exit_editing()

    def on_cancel(self):
        pass

    def _show_error_and_try_again(self):
        pass

    def _after_editing(self, user):
        pass

class NewEmployeeForm(NewAccountForm):
    def setup(self):
        pass

    def _after_editing(self, user):
        employee = None
        employee_type = self.employee_type.value
        if employee_type == "Admin":
            employee = Admin(user=user)
        elif employee_type == "Manager":
            employee = Manager(user=user)
        elif employee_type == "Mechanic":
            employee = Mechanic(user=user)
        user.employee = employee
        self.parentApp.setNextForm(employee_type)



