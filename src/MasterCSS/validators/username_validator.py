from MasterCSS.validators.validator import Validator

class UsernameValidator(Validator):

    def __init__(self):
        super().__init__("[A-Za-z0-9]+")

    def check(self, value):
        return super().check(value)

    def message(self):
        return "Invalid username format"