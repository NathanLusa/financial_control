import decimal
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver

from .common.choices import MovementTypeChoices, NoYesChoices
from .common.utils import last_day_month, first_day_month
from .models import Account, Transaction, MonthBalance, Transfer, Category


@receiver(post_save, sender=Account)
def set_initial_transaction(instance, created, **kwargs):
    movement_type = MovementTypeChoices.POSITIVE if instance.opening_balance >= 0 else MovementTypeChoices.NEGATIVE
    category = Category.objects.filter(
        is_opening_balance=NoYesChoices.YES, movement_type=movement_type).first()

    if not created and instance.initial_transaction:
        initial_transaction = instance.initial_transaction
        initial_transaction.value = instance.opening_balance
        initial_transaction.date = instance.opening_balance_date
        initial_transaction.category = category
        initial_transaction.save()
        return

    initial_transaction = Transaction()
    initial_transaction.value = decimal.Decimal(instance.opening_balance)
    initial_transaction.date = instance.opening_balance_date
    initial_transaction.description = 'OPENING BALANCE'
    initial_transaction.account = instance
    initial_transaction.category = category
    initial_transaction.save()

    instance.initial_transaction = initial_transaction

    instance.save()


@receiver(post_save, sender=Transaction)
def adjust_mounth_balance(instance, created, **kwargs):
    if created:
        date = last_day_month(instance.date)

        month_balance = MonthBalance.objects.filter(
            date=date, account=instance.account).first()
        if not month_balance:
            month_balance = MonthBalance(
                account=instance.account, date=date)

        month_balance.amount = decimal.Decimal(
            month_balance.amount) + instance.value

        month_balance.save()
    else:
        first_day = first_day_month(instance.date)
        last_day = last_day_month(instance.date)

        month_balance = MonthBalance.objects.filter(
            account=instance.account, date=last_day).first()
        if not month_balance:
            month_balance = MonthBalance(
                account=instance.account, date=last_day)

        month_balance.amount = decimal.Decimal(0.0)
        transactions = Transaction.objects.filter(account=instance.account,
                                                  date__gte=first_day, date__lte=last_day)
        for transaction in transactions:
            month_balance.amount += transaction.value

        month_balance.save()


@receiver(pre_save, sender=Transfer)
def create_transfer_transactions(instance, **kwargs):
    created = instance.pk is None
    if created:
        # criar a transacao de origem
        source_transaction = Transaction(
            value=instance.value * -1,
            date=instance.date,
            description=instance.description,
            account=instance.source,
            category=Category.objects.filter(
                is_transaction=NoYesChoices.YES, movement_type=MovementTypeChoices.NEGATIVE).first()
        )
        source_transaction.save()
        instance.source_transaction = source_transaction

        # criar a transacao de destino
        destination_transaction = Transaction(
            value=instance.value,
            date=instance.date,
            description=instance.description,
            account=instance.destination,
            category=Category.objects.filter(
                is_transaction=NoYesChoices.YES, movement_type=MovementTypeChoices.POSITIVE).first()
        )
        destination_transaction.save()
        instance.destination_transaction = destination_transaction
    else:
        source_transaction = Transaction.objects.get(
            pk=instance.source_transaction.pk)
        source_transaction.value = instance.value * -1
        source_transaction.date = instance.date
        source_transaction.description = instance.description
        source_transaction.account = instance.source
        source_transaction.save()

        destination_transaction = Transaction.objects.get(
            pk=instance.destination_transaction.pk)
        destination_transaction.value = instance.value
        destination_transaction.date = instance.date
        destination_transaction.description = instance.description
        destination_transaction.account = instance.destination
        destination_transaction.save()


@receiver(post_delete, sender=Transfer)
def delete_transfer_transactions(instance, **kwargs):
    source_transaction = Transaction.objects.get(
        pk=instance.source_transaction.pk)
    source_transaction.delete()

    destination_transaction = Transaction.objects.get(
        pk=instance.destination_transaction.pk)
    destination_transaction.delete()
