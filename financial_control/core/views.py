import decimal
from datetime import timedelta
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import AccountForm, CategoryForm, TransactionForm, TransferForm, ProgramedTransactionForm, CreditCardForm, TestForm
from .models import Account, Category, Transaction, MonthBalance, Transfer, ProgramedTransaction, CreditCard, Test

from .common import utils
from .common.choices import NoYesChoices, StatusChoices, StatusTransactionChoices


def index(request):
    return redirect('dashboard')


def process_balance(request):
    month_balances = MonthBalance.objects.all()
    for month_balance in month_balances:
        month_balance.delete()

    transactions = Transaction.objects.all().order_by('-date')
    for transaction in transactions:
        last_day = utils.last_day_month(transaction.date)

        month_balance = MonthBalance.objects.filter(
            date=last_day, account=transaction.account).first()
        if not month_balance:
            month_balance = MonthBalance(
                account=transaction.account, date=last_day)

        month_balance.amount = decimal.Decimal(
            month_balance.amount) + transaction.value
        month_balance.save()

    return redirect('dashboard')


def dashboard(request):
    accounts = Account.objects.filter(status=StatusChoices.ACTIVE)
    years = range(2015, 2021)
    months = range(1, 13)

    return render(request, 'dashboard.html', {'accounts': accounts, 'years': years, 'months': months})


def account_list(request):
    accounts = Account.objects.all()

    return render(request, 'account/account_list.html', {'accounts': accounts})


def account_new(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('account_list')
    else:
        form = AccountForm()
    return render(request, 'account/account_form.html', {'form': form})


def account_form(request, pk):
    account = get_object_or_404(Account, pk=pk)
    if request.method == 'POST':
        form = AccountForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            return redirect('account_list')
    else:
        form = AccountForm(instance=account)

    return render(request, 'account/account_form.html', {'form': form, 'id': pk})


def account_delete(request, pk):
    account = get_object_or_404(Account, pk=pk)

    # and request.user.is_authenticated and request.user.username == creator:
    if request.method == "POST":
        account.delete()

    return redirect('account_list')


def category_list(request):
    categories = Category.objects.all().exclude(
        is_transaction=NoYesChoices.YES).exclude(
        is_opening_balance=NoYesChoices.YES).order_by('description', 'id')

    return render(request, 'category/category_list.html', {'categories': categories})


def category_new(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm()

    return render(request, 'category/category_form.html', {'form': form})


def category_form(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)

    return render(request, 'category/category_form.html', {'form': form, 'id': pk})


def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)

    # and request.user.is_authenticated and request.user.username == creator:
    if request.method == "POST":
        category.delete()

    return redirect('category_list')


def transaction_list(request):
    transaction_list = Transaction.objects.all().order_by('-id')
    page = request.GET.get('page', 1)

    paginator = Paginator(transaction_list, 50)
    try:
        transactions = paginator.page(page)
    except PageNotAnInteger:
        transactions = paginator.page(1)
    except EmptyPage:
        transactions = paginator.page(paginator.num_pages)

    return render(request, 'transaction/transaction_list.html', {'transactions': transactions})


def transaction_new(request):
    if request.method == 'POST':
        next = request.GET.get('next', 'transaction_list')
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(next)
    else:
        form = TransactionForm()

    param_ajax = request.GET.get('ajax')
    param_next = request.GET.get('next', 'transaction_list')

    url_post = reverse('transaction_new') + f'?next={param_next}'

    return render(request, 'transaction/transaction_form.html', {'form': form, 'url_post': url_post, 'ajax': param_ajax})


def transaction_form(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    if request.method == 'POST':
        next = request.GET.get('next', 'transaction_list')
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect(next)
    else:
        form = TransactionForm(instance=transaction)

    param_ajax = request.GET.get('ajax')
    param_next = request.GET.get('next', 'transaction_list')

    url_post = reverse('transaction_form', args=[pk]) + f'?next={param_next}'
    url_delete = reverse('transaction_delete', args=[
                         pk]) + f'?next={param_next}'

    return render(request, 'transaction/transaction_form.html', {'form': form, 'url_post': url_post, 'url_delete': url_delete, 'ajax': param_ajax})


def transaction_delete(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)

    # and request.user.is_authenticated and request.user.username == creator:
    if request.method == "POST":
        transaction.delete()

    next = request.GET.get('next', 'transaction_list')

    return redirect(next)


def transaction_confirm(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)

    # if request.method == "POST":
    transaction.status = StatusTransactionChoices.CONFIRMED
    transaction.save()

    next = request.GET.get('next', 'transaction_list')

    return redirect(next)


def transfer_list(request):
    transfers = Transfer.objects.all().order_by('-id')

    return render(request, 'transfer/transfer_list.html', {'transfers': transfers})


def transfer_new(request):
    if request.method == 'POST':
        next = request.GET.get('next', 'transfer_list')
        form = TransferForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(next)
    else:
        form = TransferForm()

    param_ajax = request.GET.get('ajax')
    param_next = request.GET.get('next', 'transfer_list')

    url_post = reverse('transfer_new') + f'?next={param_next}'

    return render(request, 'transfer/transfer_form.html', {'form': form, 'url_post': url_post, 'ajax': param_ajax})


def transfer_form(request, pk):
    transfer = get_object_or_404(Transfer, pk=pk)
    if request.method == 'POST':
        next = request.GET.get('next', 'transfer_list')
        form = TransferForm(request.POST, instance=transfer)
        if form.is_valid():
            form.save()
            return redirect(next)
    else:
        form = TransferForm(instance=transfer)

    param_ajax = request.GET.get('ajax')
    param_next = request.GET.get('next', 'transfer_list')

    url_post = reverse('transfer_form', args=[pk]) + f'?next={param_next}'
    url_delete = reverse('transfer_delete', args=[pk]) + f'?next={param_next}'

    return render(request, 'transfer/transfer_form.html', {'form': form, 'url_post': url_post, 'url_delete': url_delete, 'ajax': param_ajax})


def transfer_delete(request, pk):
    transfer = get_object_or_404(Transfer, pk=pk)

    # and request.user.is_authenticated and request.user.username == creator:
    if request.method == "POST":
        transfer.delete()

    next = request.GET.get('next', 'transfer_list')

    return redirect(next)


def programed_transaction_list(request):
    programed_transactions = ProgramedTransaction.objects.all().order_by('-id')

    return render(request, 'programed_transaction/programed_transaction_list.html', {'programed_transactions': programed_transactions})


def programed_transaction_new(request):
    if request.method == 'POST':
        next = request.GET.get('next', 'programed_transaction_list')
        form = ProgramedTransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(next)
    else:
        form = ProgramedTransactionForm()

    param_ajax = request.GET.get('ajax')
    param_next = request.GET.get('next', 'programed_transaction_list')

    url_post = reverse('programed_transaction_new') + f'?next={param_next}'

    return render(request, 'programed_transaction/programed_transaction_form.html', {'form': form, 'url_post': url_post, 'ajax': param_ajax})


def programed_transaction_form(request, pk):
    programed_transaction = get_object_or_404(ProgramedTransaction, pk=pk)
    if request.method == 'POST':
        next = request.GET.get('next', 'programed_transaction_list')
        form = ProgramedTransactionForm(
            request.POST, instance=programed_transaction)
        if form.is_valid():
            form.save()
            return redirect(next)
    else:
        form = ProgramedTransactionForm(instance=programed_transaction)

    transactions = Transaction.objects.filter(
        programed_transaction=programed_transaction)

    param_ajax = request.GET.get('ajax')
    param_next = request.GET.get('next', 'programed_transaction_list')

    url_post = reverse('programed_transaction_form',
                       args=[pk]) + f'?next={param_next}'
    url_delete = reverse('programed_transaction_delete',
                         args=[pk]) + f'?next={param_next}'

    context = {
        'form': form,
        'transactions': transactions,
        'url_post': url_post,
        'url_delete': url_delete,
        'ajax': param_ajax,
        'pk': pk,
        'has_pendings': programed_transaction.has_pendings()
    }
    return render(request, 'programed_transaction/programed_transaction_form.html', context)


def programed_transaction_delete(request, pk):
    programed_transaction = get_object_or_404(ProgramedTransaction, pk=pk)

    # and request.user.is_authenticated and request.user.username == creator:
    if request.method == "POST":
        programed_transaction.delete()

    next = request.GET.get('next', 'programed_transaction_list')

    return redirect(next)


def programed_transaction_pending(request, pk):
    programed_transaction = get_object_or_404(ProgramedTransaction, pk=pk)
    transaction_list = programed_transaction.get_pending_transactions()

    return render(request, 'programed_transaction/programed_transaction_pending.html', {'transactions': transaction_list})


def programed_transaction_generate(request, pk, date):
    programed_transaction = get_object_or_404(ProgramedTransaction, pk=pk)
    programed_transaction.generate_transaction(date)

    return redirect('programed_transaction_pending', pk)


def programed_transaction_generate_all(request, pk):
    return programed_transaction_generate(request, pk, timedelta(days=1))


def credit_card_list(request):
    credit_cards = CreditCard.objects.all()

    return render(request, 'credit_card/credit_card_list.html', {'credit_cards': credit_cards})


def credit_card_new(request):
    if request.method == 'POST':
        form = CreditCardForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('credit_card_list')
    else:
        form = CreditCardForm()
    return render(request, 'credit_card/credit_card_form.html', {'form': form})


def credit_card_form(request, pk):
    credit_card = get_object_or_404(CreditCard, pk=pk)
    if request.method == 'POST':
        form = CreditCardForm(request.POST, instance=credit_card)
        if form.is_valid():
            form.save()
            return redirect('credit_card_list')
    else:
        form = CreditCardForm(instance=credit_card)
    return render(request, 'credit_card/credit_card_form.html', {'form': form, 'id': pk})


def credit_card_delete(request, pk):
    credit_card = get_object_or_404(CreditCard, pk=pk)

    # and request.user.is_authenticated and request.user.username == creator:
    if request.method == "POST":
        credit_card.delete()

    return redirect('credit_card_list')


def test_form(request):
    if request.method == 'POST':
        form = TestForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = TestForm()

    test_list = Test.objects.all()
    return render(request, 'test_form.html', {'form': form, 'test_list': test_list})


def test_delete(request, pk):
    test = get_object_or_404(Test, pk=pk)
    if request.method == "POST":
        test.delete()

    return redirect('test_form')
