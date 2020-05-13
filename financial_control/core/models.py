from django.db import models
from .common.enums import StatusTypes, AccountTypes, MovementTypes
from .common.models import BaseModel

class Account(BaseModel):
    description = models.CharField(max_length=50, null=False, blank=False)
    status = models.IntegerField(
        choices=StatusTypes.choices(), default=StatusTypes.ACTIVE)
    type = models.IntegerField(
        choices=AccountTypes.choices(), default=AccountTypes.CA)
    opening_balance = models.DecimalField(max_digits=10, decimal_places=2)
    opening_type = models.IntegerField(
        choices=MovementTypes.choices(), default=MovementTypes.POSITIVE)
    opening_balance_date = models.DateField()

    def __str__(self):
        return self.description

    def get_status_label(self):
        return StatusTypes(self.status).description

    def get_type_label(self):
        return AccountTypes(self.type).description

    def get_opening_type_labe(self):
        return MovementTypes(self.opening_type).description


class Category(BaseModel):
    description = models.CharField(max_length=50)
    status = models.IntegerField(
        choices=StatusTypes.choices(), default=StatusTypes.ACTIVE)
    movement_type = models.IntegerField(choices=MovementTypes.choices())

    def __str__(self):
        return self.description


class Entry(BaseModel):
    value = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    description = models.CharField(max_length=50, null=True, blank=True)
    account = models.ForeignKey(
        Account, on_delete=models.PROTECT, related_name='entries')
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    observation = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return '{} - {}'.format(self.description, self.date)
