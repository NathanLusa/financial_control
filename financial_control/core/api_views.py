import calendar
import sys
import json
from datetime import date, timedelta
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.urls import reverse

from .common import utils, exceptions
from .models import Account, Category, Transaction


def get_parameters_account_statments(request):
    # param_accounts = request.GET.get('accounts')
    param_initial_date = request.GET.get('initial_date')
    param_finish_date = request.GET.get('finish_date')

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

    return initial_date, finish_date


def get_transactions_json(transactions):
    transactions_json = []
    for transaction in transactions:
        params = '?ajax=true&next=dashboard'

        url_reverse = reverse('transaction_form', args=[transaction.id])
        url_reverse += params

        item = {
            'id': transaction.id,
            'date': transaction.date.isoformat(),
            'description': transaction.description,
            'value': transaction.value,
            'category': transaction.category.description,
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
            'value': 0.0,
        }
        accounts_json.append(item)

    return accounts_json


def accounts_statment(request):
    try:
        initial_date, finish_date = get_parameters_account_statments(request)

        accounts = Account.objects.all()
        accounts_json = get_accounts_json(accounts)

        transactions = Transaction.objects.filter(
            date__gte=initial_date, date__lte=finish_date).order_by('date', '-value')
        transactions_json = get_transactions_json(transactions)

        data = {
            'initial_date': initial_date,
            'finish_date': finish_date,
            'accounts': accounts_json,
            'transactions': transactions_json,
        }

        return JsonResponse(data)
    except exceptions.ParamError as e:
        print('Erro de parâmetro')
        return JsonResponse({'error': e.error, 'message': e.message}, status=e.error)
    except exceptions.ConverterError as ce:
        print('Erro de conversão')
        return JsonResponse({'error': ce.error, 'message': ce.message}, status=ce.error)
