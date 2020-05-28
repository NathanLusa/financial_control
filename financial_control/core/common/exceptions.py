class ParamError(Exception):
    def __init__(self, error, message):
        self.error = error
        self.message = message

    def __str__(self):
        return repr(self.error)


class ConverterError(Exception):
    def __init__(self, error, message):
        self.error = error
        self.message = message

    def __str__(self):
        return repr(self.error)
