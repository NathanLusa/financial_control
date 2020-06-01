from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import AccountForm, CategoryForm, TransactionForm
from .models import Account, Category, Transaction

from .common.choices import NoYesChoises


def dashboard(request):
    print(NoYesChoises.NO)
    return render(request, 'dashboard.html')


def account_list(request):
    accounts = Account.objects.all()

    return render(request, 'account/account_list.html', {'accounts': accounts})


def account_new(request):
    if request.method == 'POST':
        param_reverse_url = request.GET.get('reverse_url')
        form = AccountForm(request.POST)
        if form.is_valid():
            form.save()
            if param_reverse_url == 'None':
                param_reverse_url = 'account_list'
            return redirect(param_reverse_url)

    form = AccountForm()
    param_ajax = request.GET.get('ajax')
    url_post = reverse('account_new')
    param_reverse_url = request.GET.get('reverse_url')
    return render(request, 'account/account_form.html', {'form': form, 'url_post': url_post, 'ajax': param_ajax, 'reverse_url': param_reverse_url})


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
    transactions = Transaction.objects.all()

    return render(request, 'transaction/transaction_list.html', {'transactions': transactions})


def transaction_new(request):
    if request.method == 'POST':
        param_reverse_url = request.GET.get('reverse_url')
        print(param_reverse_url)
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            if param_reverse_url == 'None':
                param_reverse_url = 'transaction_list'
            return redirect(param_reverse_url)

    form = TransactionForm()
    param_ajax = request.GET.get('ajax')
    url_post = reverse('transaction_new')
    param_reverse_url = request.GET.get('reverse_url')
    return render(request, 'transaction/transaction_form.html', {'form': form, 'url_post': url_post, 'ajax': param_ajax, 'reverse_url': param_reverse_url})


def transaction_form(request, pk):
    print('transaction')
    transaction = get_object_or_404(Transaction, pk=pk)
    if request.method == 'POST':
        param_reverse_url = request.GET.get('reverse_url')
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            if param_reverse_url == 'None':
                param_reverse_url = 'transaction_list'
            return redirect(param_reverse_url)

    form = TransactionForm(instance=transaction)
    param_ajax = request.GET.get('ajax')
    url_post = reverse('transaction_form', args=[pk])
    param_reverse_url = request.GET.get('reverse_url')
    return render(request, 'transaction/transaction_form.html', {'form': form, 'id': pk, 'url_post': url_post, 'ajax': param_ajax, 'reverse_url': param_reverse_url})


def transaction_delete(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)

    # and request.user.is_authenticated and request.user.username == creator:
    if request.method == "POST":
        transaction.delete()

    return redirect('transaction_list')
