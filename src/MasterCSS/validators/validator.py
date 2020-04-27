from abc import ABC, abstractmethod
import re

class Validator(ABC):
    def __init__(self, pattern):
        self.re = re.compile(pattern)

    def check(self, value):
        return self.re.match(value)

    @abstractmethod
    def message(self):
        pass
