class OptionalIntConverter:
    regex = '[0-9]*'

    def to_python(self, value):
        if value:
            return int(value)
        else:
            return None

    def to_url(self, value):
        return str(value) if value is not None else ''
