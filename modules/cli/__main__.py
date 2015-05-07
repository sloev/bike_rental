__author__ = 'johannes'
"""__main__.py

this module does a lot of things, you can use multilines and double newlines creates sections

Attributes:
  module_level_variable (int): description of variable
"""

import npyscreen

from account import LoginForm, NewEmployeeForm
from profile import CustomerProfile, AdminProfile, ManagerProfile, MechanicProfile

import logging
logging.basicConfig(filename='bike_rental.log', level=logging.INFO)
logging.info('Started')

class MyApplication(npyscreen.NPSAppManaged):
   def onStart(self):
       self.registerForm('MAIN', LoginForm())
       self.registerForm('Customer', CustomerProfile())
       self.registerForm('Admin', AdminProfile())
       self.registerForm('Manager', ManagerProfile())
       self.registerForm('Mechanic', MechanicProfile())
       self.registerForm('NewEmployee', NewEmployeeForm())

if __name__ == '__main__':
    TestApp = MyApplication().run()