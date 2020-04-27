from MasterCSS.validators.validator import Validator

class PhoneValidator(Validator):

    def __init__(self):
        super().__init__("^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\./0-9]*$")

    def check(self, value):
        return super().check(value)

    def message(self):
        return "Invalid phone number"