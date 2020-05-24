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
        """
        Check value against regex pattern.
        
        :param value: value to check against regex.
        :type value: any
        :return: result of the check.
        :rtype: bool
        """
        return super().check(value)

    def message(self):
        """
        Get the error message.

        :return: Error message
        :rtype: string
        """
        return "Invalid username format"