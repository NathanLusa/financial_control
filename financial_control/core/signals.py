import decimal
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .common.utils import last_day_month, first_day_month
from .models import Transaction, MonthBalance


@receiver(post_save, sender=Transaction)
def adjust_mounth_balance(sender, instance, created, **kwargs):
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
