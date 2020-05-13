from django.shortcuts import get_object_or_404, render

from .forms import AccountForm
from .models import Account, Category, Entry


def index(request):
    return render(request, 'index.html')


def account_list(request):
    accounts = Account.objects.all()

    return render(request, 'account/account_list.html', {'accounts': accounts})


def account_form(request, pk):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            pass  # does nothing, just trigger the validation
    else:
        account = get_object_or_404(Account, pk=pk)
        form = AccountForm(instance=account)
    return render(request, 'account/account_form.html', {'form': form})


def category_list(request):
    categories = Category.objects.all()

    return render(request, 'category/category_list.html', {'categories': categories})


def category_form(request, pk):
    category = get_object_or_404(Category, pk=pk)

    return render(request, 'category/category_form.html', {'category': category})


def entry_list(request):
    entries = Entry.objects.all()

    return render(request, 'entry/entry_list.html', {'entries': entries})


def entry_form(request, pk):
    entry = get_object_or_404(Entry, pk=pk)

    return render(request, 'entry/entry_form.html', {'entry': entry})
