import calendar
import sys
from datetime import date, timedelta
# from django.shortcuts import get_object_or_404, redirect, render
from django.core import serializers
from django.http import JsonResponse

from .common import utils, exceptions
# from .forms import AccountForm, CategoryForm
from .models import Account, Category, Transaction
from .serializers import AccountDashboardSerializer


def dashboard(request):
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

        transactions = Transaction.objects.all()
        transactions_json = []
        # transactions_json = serializers.serialize('json', transactions)

        accounts = Account.objects.all()
        accounts_json = AccountDashboardSerializer(accounts, many=True).data
        # accounts_json = list(accounts.values())
        # accounts_json = serializers.serialize('json', accounts)

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
