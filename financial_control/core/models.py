from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils import timezone

from .common.choices import StatusChoices, AccountTypeChoices, MovementTypeChoices, NoYesChoices, FrequencyChoices, ColorChoices
from .common.models import BaseModel


class Account(BaseModel):
    description = models.CharField(max_length=25, null=False, blank=False)
    status = models.IntegerField(
        choices=StatusChoices.choices, default=StatusChoices.ACTIVE)
    type = models.IntegerField(
        choices=AccountTypeChoices.choices, default=AccountTypeChoices.CA)
    opening_balance = models.DecimalField(max_digits=10, decimal_places=2)
    opening_type = models.IntegerField(
        choices=MovementTypeChoices.choices, default=MovementTypeChoices.POSITIVE)
    opening_balance_date = models.DateField()
    color = models.IntegerField(
        choices=ColorChoices.choices, default=ColorChoices.PRIMARY)

    def __str__(self):
        return self.description

    def get_status_label(self):
        return StatusChoices(self.status).label

    def get_type_label(self):
        return AccountTypeChoices(self.type).label

    def get_opening_type_label(self):
        return MovementTypeChoices(self.opening_type).label

    def get_color_label(self):
        return ColorChoices(self.color).label


class Category(BaseModel):
    description = models.CharField(max_length=25)
    status = models.IntegerField(
        choices=StatusChoices.choices, default=StatusChoices.ACTIVE)
    movement_type = models.IntegerField(
        choices=MovementTypeChoices.choices, default=MovementTypeChoices.POSITIVE)
    is_transaction = models.IntegerField(
        choices=NoYesChoices.choices, default=int(NoYesChoices.NO))

    def __str__(self):
        return self.description

    def get_status_label(self):
        return StatusChoices(self.status).label

    def get_movement_type_label(self):
        return MovementTypeChoices(self.movement_type).label

    def is_expense(self):
        return self.movement_type == MovementTypeChoices.NEGATIVE

    def is_active(self):
        return self.status == StatusChoices.ACTIVE


class Transaction(BaseModel):
    value = models.DecimalField(max_digits=15, decimal_places=2, default=0.0)
    date = models.DateField()
    description = models.CharField(max_length=100, null=True, blank=True)
    account = models.ForeignKey(
        Account, on_delete=models.PROTECT, related_name='transactions')
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    observation = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f'({self.account}) {self.description} - {self.date}'


class MonthBalance(BaseModel):
    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, null=False, related_name='month_balances')
    date = models.DateField()
    amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.0)

    class Meta:
        unique_together = ('account', 'date')

    def __str__(self):
        return f'{self.date} - {self.amount}'


class Transfer(BaseModel):
    source = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name='account_sources')
    destination = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name='account_destinations')
    date = models.DateField(default=timezone.now)
    value = models.DecimalField(max_digits=15, decimal_places=2, default=0.0)
    description = models.CharField(max_length=100, null=True, blank=True)
    source_transaction = models.ForeignKey(
        Transaction, on_delete=models.CASCADE, related_name='source_transaction')
    destination_transaction = models.ForeignKey(
        Transaction, on_delete=models.CASCADE, related_name='destination_transaction')

    def __str__(self):
        return f'Transfer from "{self.source}" to "{self.destination}"'


class ProgramedTransaction(BaseModel):
    initial_date = models.DateField(default=timezone.now)
    account = models.ForeignKey(
        Account, on_delete=models.PROTECT, related_name='programed_transactions')
    frequency = models.IntegerField(
        choices=FrequencyChoices.choices, default=FrequencyChoices.DIARY)
    value = models.DecimalField(max_digits=15, decimal_places=2, default=0.0)
    description = models.CharField(max_length=100, null=True, blank=True)
    observation = models.CharField(max_length=200, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    last_verification = models.DateField(null=True, blank=True)
    status = models.IntegerField(
        choices=StatusChoices.choices, default=StatusChoices.ACTIVE)
    transaction = GenericRelation(Transaction)

    def __str__(self):
        return self.description

    def get_frequency_label(self):
        return FrequencyChoices(self.frequency).label

    def get_status_label(self):
        return StatusChoices(self.status).label
