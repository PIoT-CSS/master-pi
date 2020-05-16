from MasterCSS.validators.validator import Validator

class EmailValidator(Validator):
    """
    EmailValidator classes.
    """
    def __init__(self):
        """
        Init with an email regex pattern.
        Reference: https://stackoverflow.com/questions/742451/what-is-the-
        simplest-regular-expression-to-validate-emails-to-not-accept-them-bl
        """
        super().__init__("(?!.*\.\.)(^[^\.][^@\s]+@[^@\s]+\.[^@\s\.]+$)")

    def check(self, value):
        return super().check(value)

    def message(self):
        return "Invalid email format"