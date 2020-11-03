from calendar import month, monthrange
from datetime import date, timedelta
from django.db import models
from django.utils import timezone

from .common.model_fields import IntegerRangeField
from .common.choices import StatusChoices, AccountTypeChoices, MovementTypeChoices, NoYesChoices, FrequencyChoices, ColorChoices, StatusTransactionChoices
from .common.models import BaseModel, ObjectFactory


class Account(BaseModel):
    description = models.CharField(max_length=25, null=False, blank=False)
    status = models.IntegerField(
        choices=StatusChoices.choices, default=StatusChoices.ACTIVE)
    type = models.IntegerField(
        choices=AccountTypeChoices.choices, default=AccountTypeChoices.CA)
    opening_balance = models.DecimalField(max_digits=15, decimal_places=2)
    opening_type = models.IntegerField(
        choices=MovementTypeChoices.choices, default=MovementTypeChoices.POSITIVE)
    opening_balance_date = models.DateField()
    color = models.IntegerField(
        choices=ColorChoices.choices, default=ColorChoices.PRIMARY)
    initial_transaction = models.OneToOneField(
        'Transaction', on_delete=models.CASCADE, related_name='initial_transaction', null=True)

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
        choices=MovementTypeChoices.choices, default=MovementTypeChoices.NEGATIVE)
    is_transaction = models.IntegerField(
        choices=NoYesChoices.choices, default=int(NoYesChoices.NO))
    is_opening_balance = models.IntegerField(
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
        Account, on_delete=models.CASCADE, related_name='transactions')
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    observation = models.CharField(max_length=200, null=True, blank=True)
    status = models.IntegerField(
        choices=StatusTransactionChoices.choices, default=StatusTransactionChoices.CONFIRMED)
    programed_transaction = models.ForeignKey(
        "ProgramedTransaction", on_delete=models.CASCADE, related_name='transactions', null=True, blank=True)

    def __str__(self):
        return f'({self.account}) {self.description} - {self.date} - ${self.value}'

    def get_status_label(self):
        return StatusTransactionChoices(self.status).label

    def get_status_color(self):
        switcher = {
            0: 'info',
            1: 'warning',
            2: 'success',
            3: 'danger'
        }
        return switcher[self.status]

    def is_pending(self):
        return self.status == StatusTransactionChoices.PENDING


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
        Account, on_delete=models.CASCADE, related_name='programed_transactions')
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

    def get_date_to_validate(self):
        today = date.today()
        date_to_validate = today.replace(
            day=monthrange(today.year, today.month)[1])

        return date_to_validate

    def generate_transaction(self, dt):
        generator = self.Generator(self)
        transactions = generator.get_transactions(dt)

        for transaction in transactions:
            transaction.save()

    def get_pending_transactions(self):
        date_to_validate = self.get_date_to_validate()
        pendings = []
        if (self.last_verification or (date_to_validate + timedelta(-1))) < date_to_validate and self.initial_date < date_to_validate:
            generator = self.Generator(self)
            pendings = generator.get_transactions(timedelta(days=1))

        return pendings

    class Generator:
        def __init__(self, programed_transaction):
            self.programed_transaction = programed_transaction
            self.factory = ObjectFactory()
            self._register()
            self._transactions = list(Transaction.objects.filter(
                programed_transaction=programed_transaction))

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
            builder = self.factory.create(
                frequency, transactions=self._transactions)

            return builder.generate(self.programed_transaction, dt)

        class BaseGenerator:
            def __init__(self, transactions):
                self._transactions = transactions

            def get_next_day(self, day):
                pass

            def generate(self, programed_transaction, dt):
                transaction_list = []
                min_date = timedelta(days=1)
                day = programed_transaction.initial_date
                date_to_validade = programed_transaction.get_date_to_validate()

                while day <= date_to_validade:
                    if (dt == min_date) or (day == dt.date()):
                        transaction = [
                            t for t in self._transactions if t.date == day]
                        if not transaction:
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
                            self._transactions.append(transaction)

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
                days_in_month = monthrange(day.year, day.month)[1]
                return day + timedelta(days=days_in_month)

            def generate(self, programed_transaction, dt):
                return super().generate(programed_transaction, dt)

        class YearlyGenerator(BaseGenerator):
            def get_next_day(self, day):
                return day.replace(year=day.year + 1)

            def generate(self, programed_transaction, dt):
                return super().generate(programed_transaction, dt)


class CreditCard(BaseModel):
    description = models.CharField(max_length=100, null=False, blank=False)
    payment_day = IntegerRangeField(min_value=1, max_value=31)
    payment_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='credit_cards')


class CreditCardInvoice(BaseModel):
    credit_card = models.ForeignKey(CreditCard, on_delete=models.CASCADE, related_name='invoices')
    payment_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='credit_card_invoices')
    payment_date = models.DateField()
    payment_transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE, related_name='credit_card_invoice_payment')
    is_open = models.IntegerField(choices=NoYesChoices.choices, default=int(NoYesChoices.YES))

    def get_is_open_label(self):
        return NoYesChoices(self.is_open).label


class CreditCardInvoiceDetail(BaseModel):
    credit_card_invoice = models.ForeignKey(CreditCardInvoice, on_delete=models.CASCADE, related_name='invoice_details')
    description = models.CharField(max_length=100, null=True, blank=True)
    value = models.DecimalField(max_digits=15, decimal_places=2, default=0.0)
    date = models.DateField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    observation = models.CharField(max_length=200, null=True, blank=True)
