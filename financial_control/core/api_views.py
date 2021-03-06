import calendar
import sys
import json
import decimal
from datetime import date, timedelta
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.urls import reverse

from .common import utils, exceptions
from .common.choices import ColorChoices, StatusTransactionChoices
from .models import Account, Category, Transaction, MonthBalance, ProgramedTransaction


def get_parameters_account_statments(request):
    # param_accounts = request.GET.get('accounts')
    param_initial_date = request.GET.get('initial_date')
    param_finish_date = request.GET.get('finish_date')
    param_accounts = request.GET.get('accounts')
    param_description = request.GET.get('description')

    if not param_initial_date:
        raise exceptions.ParamError(
            400, 'The param initial_date is not set.')

    if not param_finish_date:
        raise exceptions.ParamError(
            400, 'The param finish_date is not set.')

    initial_date = utils.str_to_date(param_initial_date)
    finish_date = utils.str_to_date(param_finish_date)

    if initial_date > finish_date:
        finish_date = utils.last_day_month(initial_date)

    account_list = [0] if param_accounts == '' else param_accounts.split(',')

    return initial_date, finish_date, account_list, param_description


def get_transactions_json(transactions):
    transactions_json = []
    for transaction in transactions:
        params = '?ajax=true&next=dashboard'

        url_reverse = reverse('transaction_form', args=[transaction.id])
        url_reverse += params

        item = {
            'id': transaction.id,
            'date': transaction.date.isoformat(),
            'account': {
                'id': transaction.account.id,
                'description': transaction.account.description,
                'color': ColorChoices(transaction.account.color).label
            },
            'description': transaction.description,
            'value': transaction.value,
            'category': transaction.category.description,
            'status': transaction.get_status_label(),
            'status_color': transaction.get_status_color(),
            'url': url_reverse
        }
        transactions_json.append(item)

    return transactions_json


def get_accounts_json(accounts):
    accounts_json = []

    for account in accounts:
        item = {
            'id': account.id,
            'description': account.description,
            'value': decimal.Decimal(0.0),
            'color': account.color
        }
        accounts_json.append(item)

    return accounts_json


def get_month_balance_json(month_balances, transactions, accounts):
    month_balances_json = []

    for account in accounts:
        prev_amount = decimal.Decimal(0)

        months = month_balances.filter(account=account.id)
        for month in months:
            prev_amount += month.amount

        income_value = decimal.Decimal(0)
        expense_value = decimal.Decimal(0)
        min_date_transaction = date.today()

        transaction_list = transactions.filter(account=account.id)
        min_transaction = transaction_list.order_by('date').first()
        if min_transaction:
            min_date_transaction = utils.first_day_month(
                min_transaction.date) - timedelta(1)

        for transaction in transaction_list:
            if transaction.value >= 0:
                income_value += transaction.value
            else:
                expense_value += transaction.value

        amount = income_value + expense_value

        month = months.order_by('date').last()
        if not month:
            month = MonthBalance(id=0, account=account,
                                 date=min_date_transaction)

        item = {
            'id': month.id,
            'account': {
                'id': month.account.id,
                'description': month.account.description,
                'color': ColorChoices(month.account.color).label
            },
            'date': month.date,
            'income_value': income_value,
            'expense_value': expense_value,
            'amount': amount,
            'prev_amount': prev_amount,
            'accumulated': prev_amount + amount
        }
        month_balances_json.append(item)

    return month_balances_json


def accounts_statment(request):
    try:
        initial_date, finish_date, accounts_filter, description = get_parameters_account_statments(
            request)

        accounts = Account.objects.filter(pk__in=accounts_filter)
        accounts_json = get_accounts_json(accounts)

        transactions = Transaction.objects.filter(account__in=accounts_filter,
                                                  date__gte=initial_date, date__lte=finish_date, description__icontains=description).order_by('date', '-value')
        transactions_json = get_transactions_json(transactions)

        month_balances = MonthBalance.objects.filter(account__in=accounts_filter,
                                                     date__lt=initial_date).order_by('date')
        month_balances_json = get_month_balance_json(
            month_balances, transactions, accounts)

        data = {
            'initial_date': initial_date,
            'finish_date': finish_date,
            'accounts': accounts_json,
            'transactions': transactions_json,
            'month_balances': month_balances_json
        }

        return JsonResponse(data)
    except exceptions.ParamError as e:
        print('Erro de parâmetro')
        return JsonResponse({'error': e.error, 'message': e.message}, status=e.error)
    except exceptions.ConverterError as ce:
        print('Erro de conversão')
        return JsonResponse({'error': ce.error, 'message': ce.message}, status=ce.error)


def notifications(request):
    notifications = []
    programed_transaction_list = ProgramedTransaction.objects.all()
    for prog_transaction in programed_transaction_list:
        if prog_transaction.has_pendings():
            notifications.append({
                'description': prog_transaction.description,
                'url': reverse('programed_transaction_pending', args=[prog_transaction.id])
            })

    data = {
        'notifications': notifications
    }
    return JsonResponse(data)
