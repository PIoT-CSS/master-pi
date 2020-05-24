class ErrorValueException(Exception):
    """
    Error Value Exception for serverside on REST payload
    """

    def __init__(self, message, payload=None):
        Exception.__init__(self)
        self.message = message
        self.payload = payload
