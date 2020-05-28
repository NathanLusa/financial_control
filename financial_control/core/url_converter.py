class OptionalIntConverter:
    regex = '[0-9]*'

    def to_python(self, value):
        if value:
            return int(value)
        else:
            return None

    def to_url(self, value):
        return str(value) if value is not None else ''


# class Date:
#     regex = '^(19[0-9]{2}|2[0-9]{3})-(0[1-9]|1[012])-([123]0|[012][1-9]|31)$'

#     def to_python(self, value):
#         return none

#     def to_url(self, value):
#         return str(value) if value is not None else ''
