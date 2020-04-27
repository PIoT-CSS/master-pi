from MasterCSS.validators.validator import Validator

class EmailValidator(Validator):

    def __init__(self):
        super().__init__("(?!.*\.\.)(^[^\.][^@\s]+@[^@\s]+\.[^@\s\.]+$)")

    def check(self, value):
        return super().check(value)

    def message(self):
        return "Invalid email format"