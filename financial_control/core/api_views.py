from django.core.serializers.json import DjangoJSONEncoder
import calendar
import sys
import json
from datetime import date, timedelta
from django.http import JsonResponse

from .common import utils, exceptions
from .models import Account, Category, Transaction


def accounts_statment(request):
    param_accounts = request.GET.get('accounts')
    param_initial_date = request.GET.get('initial_date')
    param_finish_date = request.GET.get('finish_date')

    try:
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

        transactions_json = []
        transactions = Transaction.objects.filter(
            date__gte=initial_date, date__lte=finish_date)
        for transaction in transactions:
            item = {
                'date': transaction.date,
                'description': transaction.description,
                'value': transaction.value,
                'category': transaction.category.description,
            }
            transactions_json.append(item)

        accounts_json = []
        accounts = Account.objects.all()
        for account in accounts:
            item = {
                'id': account.id,
                'description': account.description,
                'value': 0,
            }
            accounts_json.append(item)

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
