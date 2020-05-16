from MasterCSS.validators.validator import Validator

class UsernameValidator(Validator):
    """
    UsernameValidator classes.
    """
    def __init__(self):
        """
        Init with regex pattern:
        - An username may not contain any special characters or spaces.
        """
        super().__init__("[A-Za-z0-9]+")

    def check(self, value):
        return super().check(value)

    def message(self):
        return "Invalid username format"