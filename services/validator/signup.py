# -*- coding: utf-8 -*-
'''
    validator.signup
    -------------------------
    The signup class.
'''

from .validator import ValidatorInterface
from Models.users import User


class SignUp(ValidatorInterface):

    typeExpected = {'username': str, 'password': str, 'email': str}

    def __init__(self, data):
        self.data = data
        self.errors = {'blank_fields': [], 'invalid_type_fields': []}

    def is_valid(self):
        checkType =  map(lambda x: True if (type(self.data[x]) == SignUp.typeExpected[x]) else self.errors['invalid_type_fields'].append(x),self.data)
        checkEmpty = map(lambda x: True if (self.data[x]) else self.errors['blank_fields'].append(x),self.data)

        x = all(list(checkEmpty))
        y = all(list(checkType))
        if x and y: return True
        pass


    def iter_errors(self):
        checkType =  map(lambda x: True if (type(self.data[x]) == SignUp.typeExpected[x]) else self.errors['invalid_type_fields'].append(x),self.data)
        checkEmpty = map(lambda x: True if (self.data[x]) else self.errors['blank_fields'].append(x),self.data)

        return self.errors
        pass


    def check_password(self, password):
        length = len(password) >= 6
        case = password != password.upper() and password != password.lower()
        digit = any(c.isdigit() for c in password)

        return (length and case and digit == True)


    def unique_fields(self, data):
        user_by_username = User.query.filter_by(username=data['username']).first()
        user_by_email = User.query.filter_by(email=data['email']).first()

        if not (user_by_username or user_by_email):
            return True
        return False

