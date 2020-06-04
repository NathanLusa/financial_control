from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import AccountForm, CategoryForm, TransactionForm
from .models import Account, Category, Transaction

from .common.choices import NoYesChoises


def index(request):
    return redirect('dashboard')


def dashboard(request):
    return render(request, 'dashboard.html')


def account_list(request):
    accounts = Account.objects.all()

    return render(request, 'account/account_list.html', {'accounts': accounts})


def account_new(request):
    if request.method == 'POST':
        next = request.GET.get('next', 'account_list')
        form = AccountForm(request.POST)
        if form.is_valid():
            form.save()

            return redirect(next)

    form = AccountForm()
    param_ajax = request.GET.get('ajax')
    url_post = reverse('account_new')
    param_next = request.GET.get('next')
    return render(request, 'account/account_form.html', {'form': form, 'url_post': url_post, 'ajax': param_ajax, 'next': param_next})


def account_form(request, pk):
    account = get_object_or_404(Account, pk=pk)
    if request.method == 'POST':
        form = AccountForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            return redirect('account_list')

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
        is_transaction=NoYesChoises.YES).order_by('description', 'id')

    return render(request, 'category/category_list.html', {'categories': categories})


def category_new(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')

    form = CategoryForm()
    return render(request, 'category/category_form.html', {'form': form})


def category_form(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list')

    form = CategoryForm(instance=category)
    return render(request, 'category/category_form.html', {'form': form, 'id': pk})


def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)

    # and request.user.is_authenticated and request.user.username == creator:
    if request.method == "POST":
        category.delete()

    return redirect('category_list')


def transaction_list(request):
    transactions = Transaction.objects.all().order_by('-id')

    return render(request, 'transaction/transaction_list.html', {'transactions': transactions})


def transaction_new(request):
    if request.method == 'POST':
        next = request.GET.get('next', 'transaction_list')
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()

            return redirect(next)
        else:
            print(f'errors: {form.errors}')
            return JsonResponse({'error': 500, 'message': form.errors}, status=400)

    form = TransactionForm()
    param_ajax = request.GET.get('ajax')
    url_post = reverse('transaction_new')
    param_next = request.GET.get('next')
    return render(request, 'transaction/transaction_form.html', {'form': form, 'url_post': url_post, 'ajax': param_ajax, 'next': param_next})


def transaction_form(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    if request.method == 'POST':
        next = request.GET.get('next', 'transaction_list')
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()

            return redirect(next)
        else:
            print(f'errors: {form.errors}')

    param_ajax = request.GET.get('ajax')
    param_next = request.GET.get('next')

    form = TransactionForm(instance=transaction)
    url_post = reverse('transaction_form', args=[pk])

    next_url = ''
    next_transaction_list = Transaction.objects.all().order_by('date', '-value')
    # next_transaction_list.get(pk=pk)
    next_transaction = False
    if next_transaction:
        next_url = reverse('transaction_form', args=[next_transaction.id])

    return render(request, 'transaction/transaction_form.html', {'form': form, 'id': pk, 'url_post': url_post, 'ajax': param_ajax, 'next': param_next, 'next_url': next_url})


def transaction_delete(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)

    # and request.user.is_authenticated and request.user.username == creator:
    if request.method == "POST":
        transaction.delete()

    return redirect('transaction_list')
