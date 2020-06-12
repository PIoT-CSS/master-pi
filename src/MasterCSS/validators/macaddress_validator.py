from MasterCSS.validators.validator import Validator

class MacAddressValidator(Validator):
    """
    MacAddressValidator classes.
    """
    def __init__(self):
        """
        Init with a mac address regex pattern.
        Reference: https://stackoverflow.com/questions/4260467/
        what-is-a-regular-expression-for-a-mac-address
        """
        super().__init__("^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$")

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
        return "Invalid Mac Address"