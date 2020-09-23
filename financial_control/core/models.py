import abc
from calendar import month, monthrange
from datetime import date, timedelta
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils import timezone

from .common.choices import StatusChoices, AccountTypeChoices, MovementTypeChoices, NoYesChoices, FrequencyChoices, ColorChoices, StatusTransactionChoices
from .common.models import BaseModel, ObjectFactory


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
    status = models.IntegerField(
        choices=StatusTransactionChoices.choices, default=StatusTransactionChoices.CONFIRMED)
    programed_transaction = models.ForeignKey(
        "ProgramedTransaction", on_delete=models.CASCADE, related_name='transactions', null=True, blank=True)

    def __str__(self):
        return f'({self.account}) {self.description} - {self.date}'

    def get_status_label(self):
        return StatusTransactionChoices(self.status).label

    def get_status_color(self):
        # PENDING = 0, _('Pending')
        # SCHEDULED = 1, _('Scheduled')
        # CONFIRMED = 2, _('Confirmed')
        # CANCELED = 3, _('Canceled')

        switcher = {
            0: 'info',
            1: 'warning',
            2: 'success',
            3: 'danger'
        }
        return switcher[self.status]


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

    def __str__(self):
        return self.description

    def get_frequency_label(self):
        return FrequencyChoices(self.frequency).label

    def get_status_label(self):
        return StatusChoices(self.status).label

    def has_pendings(self):
        transactions = self.get_pending_transactions()
        return len(transactions) > 0

    def generate_transaction(self, dt):
        generator = self.Generator(self)
        transactions = generator.get_transactions(dt)

        for transaction in transactions:
            transaction.save()

    def get_pending_transactions(self):
        today = date.today()
        pendings = []

        if (self.last_verification or (today + timedelta(-1))) < today and self.initial_date < today:
            generator = self.Generator(self)
            pendings = generator.get_transactions(timedelta(days=1))

        return pendings

    class Generator:
        def __init__(self, programed_transaction):
            self.programed_transaction = programed_transaction
            self.factory = ObjectFactory()
            self._register()

        def _register(self):
            self.factory.register_builder(
                FrequencyChoices.DIARY, self.DiaryGenerator)
            self.factory.register_builder(
                FrequencyChoices.WEEKLY, self.WeeklyGenerator)
            self.factory.register_builder(
                FrequencyChoices.MONTHLY, self.MonthlyGenerator)
            self.factory.register_builder(
                FrequencyChoices.YEARLY, self.YearlyGenerator)

        def get_transactions(self, dt):
            frequency = FrequencyChoices(self.programed_transaction.frequency)
            builder = self.factory.create(frequency)

            return builder.generate(self.programed_transaction, dt)

        class BaseGenerator:
            def get_next_day(self, day):
                pass

            def generate(self, programed_transaction, dt):
                transaction_list = []
                min_date = timedelta(days=1)
                day = programed_transaction.initial_date

                while day <= date.today():
                    if (dt == min_date) or (day == dt.date()):
                        transactions = programed_transaction.transactions.filter(
                            date=day)
                        if transactions.count() == 0:
                            transaction = Transaction(
                                value=programed_transaction.value,
                                date=day,
                                description=programed_transaction.description,
                                observation=programed_transaction.observation,
                                account=programed_transaction.account,
                                category=programed_transaction.category,
                                status=StatusTransactionChoices.PENDING,
                                programed_transaction=programed_transaction
                            )
                            transaction_list.append(transaction)

                    day = self.get_next_day(day)

                return transaction_list

        class DiaryGenerator(BaseGenerator):
            def get_next_day(self, day):
                return day + timedelta(days=1)

            def generate(self, programed_transaction, dt):
                return super().generate(programed_transaction, dt)

        class WeeklyGenerator(BaseGenerator):
            def get_next_day(self, day):
                return day + timedelta(days=7)

            def generate(self, programed_transaction, dt):
                return super().generate(programed_transaction, dt)

        class MonthlyGenerator(BaseGenerator):
            def get_next_day(self, day):
                year = day.year
                month = day.month + 1
                if month > 12:
                    month = 1
                    year += 1

                days_in_month = monthrange(year, month)[1]
                return day + timedelta(days=days_in_month)

            def generate(self, programed_transaction, dt):
                return super().generate(programed_transaction, dt)

        class YearlyGenerator(BaseGenerator):
            def get_next_day(self, day):
                return day.replace(year=day.year + 1)

            def generate(self, programed_transaction, dt):
                return super().generate(programed_transaction, dt)
