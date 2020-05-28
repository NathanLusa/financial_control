from django.shortcuts import get_object_or_404, redirect, render

from .forms import AccountForm, CategoryForm
from .models import Account, Category, Transaction


def dashboard(request):
    return render(request, 'dashboard.html')


def account_list(request):
    accounts = Account.objects.all()

    return render(request, 'account/account_list.html', {'accounts': accounts})


def account_new(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('account_list')

    form = AccountForm()
    return render(request, 'account/account_form.html', {'form': form})


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
    categories = Category.objects.all()
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


def transaction_form(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)

    return render(request, 'transaction/transaction_form.html', {'transaction': transaction, 'id': pk})


def transaction_delete(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)

    # and request.user.is_authenticated and request.user.username == creator:
    if request.method == "POST":
        transaction.delete()

    return redirect('transaction_list')
