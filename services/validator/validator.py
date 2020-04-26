# -*- coding: utf-8 -*-
'''
    validator.validator
    -------------------------
    The validator interface.
'''


from abc import ABC, abstractmethod

class ValidatorInterface(ABC):

    @abstractmethod
    def is_valid(self):
        pass

    @abstractmethod
    def iter_errors(self):
        pass

    @abstractmethod
    def check_password(self, password):
        pass

    @abstractmethod
    def unique_fields(self, data):
        pass
