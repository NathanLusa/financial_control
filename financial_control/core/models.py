from django.db import models
from .common.choices import StatusChoises, AccountTypeChoises, MovementTypeChoises, NoYesChoises
from .common.models import BaseModel


class Account(BaseModel):
    description = models.CharField(max_length=25, null=False, blank=False)
    status = models.IntegerField(
        choices=StatusChoises.choices, default=StatusChoises.ACTIVE)
    type = models.IntegerField(
        choices=AccountTypeChoises.choices, default=AccountTypeChoises.CA)
    opening_balance = models.DecimalField(max_digits=10, decimal_places=2)
    opening_type = models.IntegerField(
        choices=MovementTypeChoises.choices, default=MovementTypeChoises.POSITIVE)
    opening_balance_date = models.DateField()

    def __str__(self):
        return self.description

    def get_status_label(self):
        return StatusChoises(self.status).label

    def get_type_label(self):
        return AccountTypeChoises(self.type).label

    def get_opening_type_labe(self):
        return MovementTypeChoises(self.opening_type).label


class Category(BaseModel):
    description = models.CharField(max_length=25)
    status = models.IntegerField(
        choices=StatusChoises.choices, default=StatusChoises.ACTIVE)
    movement_type = models.IntegerField(
        choices=MovementTypeChoises.choices, default=MovementTypeChoises.POSITIVE)
    is_transaction = models.IntegerField(
        choices=NoYesChoises.choices, default=int(NoYesChoises.NO))

    def __str__(self):
        return self.description

    def get_status_label(self):
        return StatusChoises(self.status).label

    def get_movement_type_label(self):
        return MovementTypeChoises(self.movement_type).label

    def is_expense(self):
        return self.movement_type == MovementTypeChoises.NEGATIVE

    def is_active(self):
        return self.status == StatusChoises.ACTIVE


class Transaction(BaseModel):
    value = models.DecimalField(max_digits=15, decimal_places=2, default=0.0)
    date = models.DateField()
    description = models.CharField(max_length=100, null=True, blank=True)
    account = models.ForeignKey(
        Account, on_delete=models.PROTECT, related_name='transactions')
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    observation = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return '{} - {}'.format(self.description, self.date)


class MonthBalance(BaseModel):
    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, null=False, related_name='month_balances')
    date = models.DateField()
    amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.0)

    class Meta:
        unique_together = ('account', 'date')

    def __str__(self):
        return f'{self.date} - {self.amount}'
