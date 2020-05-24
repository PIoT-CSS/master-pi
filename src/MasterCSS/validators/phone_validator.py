from MasterCSS.validators.validator import Validator

class PhoneValidator(Validator):
    """
    PhoneValidator classes.
    """
    def __init__(self):
        """
        Init with a phone regex pattern.
        Reference: https://stackoverflow.com/questions/59154144/
        regex-check-for-variations-of-phone-number
        """
        super().__init__("^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\./0-9]*$")

    def check(self, value):
        """
        Check value against regex pattern.

        :param value: A value to be checked
        :type value: String, int,...
        :return: Check if it is valid.
        :rtype: Boolean
        """
        return super().check(value)

    def message(self):
        return "Invalid phone number"