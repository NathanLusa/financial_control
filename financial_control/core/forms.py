from datetime import date
from django import forms
from django.forms import ModelForm

from .models import Account, Category, Transaction
from .fields import DateField  # , CharField, TimeField


class AccountForm(ModelForm):

    opening_balance_date = DateField(autofocus=True)

    class Meta:
        model = Account
        fields = ['description', 'status', 'type', 'opening_balance',
                  'opening_type', 'opening_balance_date']


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['description', 'status', 'movement_type']

    # name = forms.CharField(max_length=30)
    # email = forms.EmailField(max_length=254)
    # message = forms.CharField(
    #     max_length=2000,
    #     widget=forms.Textarea(),
    #     help_text='Write here your message!'
    # )
    # source = forms.CharField(       # A hidden input for internal use
    #     max_length=50,              # tell from which page the user sent the message
    #     widget=forms.HiddenInput()
    # )

    # def clean(self):
    #     cleaned_data = super(AccountForm, self).clean()
    #     name = cleaned_data.get('name')
    #     email = cleaned_data.get('email')
    #     message = cleaned_data.get('message')
    #     if not name and not email and not message:
    #         raise forms.ValidationError('You have to write something!')


class TransactionForm(ModelForm):

    date = DateField(value=date.today())

    class Meta:
        model = Transaction
        fields = ['account', 'date', 'value',
                  'description', 'observation', 'category']

    # value = models.DecimalField(max_digits=10, decimal_places=2)
    # date = models.DateField()
    # description = models.CharField(max_length=50, null=True, blank=True)
    # account = models.ForeignKey(
    #     Account, on_delete=models.PROTECT, related_name='transactions')
    # category = models.ForeignKey(Category, on_delete=models.PROTECT)
    # observation = models.CharField(max_length=200, null=True, blank=True)
