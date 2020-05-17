from abc import ABC, abstractmethod
import re

class Validator(ABC):
    """
    Abstract validator classes.
    """
    def __init__(self, pattern):
        """
        Constructor. 

        :param pattern: Regex string
        :type pattern: string
        """
        self.re = re.compile(pattern)

    def check(self, value):
        """
        Check value against regex pattern.
        
        :param value: value to check against regex.
        :type value: any
        :return: result of the check.
        :rtype: bool
        """
        return self.re.match(value)

    @abstractmethod
    def message(self):
        """
        Return the error message
        """
        pass
