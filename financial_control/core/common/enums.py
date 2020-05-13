from enum import Enum


class BaseEnum(Enum):
    def __new__(cls, keycode, name):
        obj = object.__new__(cls)
        obj._value_ = keycode
        obj.description = name
        return obj

    @classmethod
    def choices(cls):
        return [(key.value, key.description) for key in cls]


class StatusTypes(BaseEnum):
    INACTIVE = 0, 'Inactive'
    ACTIVE = 1, 'Active'


class AccountTypes(BaseEnum):
    CA = 0, 'Checking Account'
    MO = 1, 'Money'
    OT = 2, 'Other'


class MovementTypes(BaseEnum):
    NEGATIVE = 0, 'Negative'
    POSITIVE = 1, 'Positive'
