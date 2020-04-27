class ErrorValueException(Exception):

    def __init__(self, message, payload=None):
        Exception.__init__(self)
        self.message = message
        self.payload = payload