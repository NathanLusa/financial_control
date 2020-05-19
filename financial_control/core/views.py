from django.shortcuts import get_object_or_404, redirect, render

from .forms import AccountForm, CategoryForm
from .models import Account, Category, Entry


def index(request):
    return render(request, 'index.html')


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


def entry_list(request):
    entries = Entry.objects.all()

    return render(request, 'entry/entry_list.html', {'entries': entries})


def entry_form(request, pk):
    entry = get_object_or_404(Entry, pk=pk)

    return render(request, 'entry/entry_form.html', {'entry': entry, 'id': pk})


def entry_delete(request, pk):
    entry = get_object_or_404(Entry, pk=pk)

    # and request.user.is_authenticated and request.user.username == creator:
    if request.method == "POST":
        entry.delete()

    return redirect('entry_list')
