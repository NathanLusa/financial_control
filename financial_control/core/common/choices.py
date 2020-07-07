# from enum import Enum
from django.db.models import IntegerChoices
from django.utils.translation import gettext_lazy as _


# class BaseEnum(Enum):
#     def __new__(cls, keycode, name):
#         obj = object.__new__(cls)
#         obj._value_ = keycode
#         obj.description = name
#         return obj

#     @classmethod
#     def choices(cls):
#         return [(key.value, key.description) for key in cls]


class NoYesChoices(IntegerChoices):
    NO = 0, _('No')
    YES = 1, _('Yes')


class StatusChoices(IntegerChoices):
    INACTIVE = 0, _('Inactive')
    ACTIVE = 1, _('Active')


class AccountTypeChoices(IntegerChoices):
    CA = 0, _('Checking Account')
    MO = 1, _('Money')
    OT = 2, _('Other')


class MovementTypeChoices(IntegerChoices):
    NEGATIVE = 0, _('Negative')
    POSITIVE = 1, _('Positive')


class FrequencyChoices(IntegerChoices):
    DIARY = 0, _('Diary')
    WEEKLY = 1, _('Weekly')
    MONTHLY = 2, _('Monthly')
    YEARLY = 3, _('Yearly')
