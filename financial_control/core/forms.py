from datetime import date
from django import forms
from django.forms import ModelForm, Form

from .models import Account, Category, Transaction, Transfer, ProgramedTransaction, CreditCard, Test
from .fields import DateField  # , CharField, TimeField


class AccountForm(ModelForm):

    opening_balance_date = DateField(autofocus=True)

    class Meta:
        model = Account
        fields = ['description', 'status', 'type', 'opening_balance',
                  'opening_type', 'opening_balance_date', 'color']


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

    date = DateField()

    class Meta:
        model = Transaction
        fields = ['account', 'date', 'value', 'description',
                  'observation', 'category', 'status']

    # value = models.DecimalField(max_digits=10, decimal_places=2)
    # date = models.DateField()
    # description = models.CharField(max_length=50, null=True, blank=True)
    # account = models.ForeignKey(
    #     Account, on_delete=models.PROTECT, related_name='transactions')
    # category = models.ForeignKey(Category, on_delete=models.PROTECT)
    # observation = models.CharField(max_length=200, null=True, blank=True)


class TransferForm(ModelForm):

    date = DateField()

    class Meta:
        model = Transfer
        fields = ['source', 'destination', 'date', 'value', 'description']


class ProgramedTransactionForm(ModelForm):

    initial_date = DateField()

    class Meta:
        model = ProgramedTransaction
        fields = ['initial_date', 'account', 'frequency', 'value',
                  'description', 'observation', 'category', 'status']


class CreditCardForm(ModelForm):

    class Meta:
        model = CreditCard
        fields = ['description', 'name_on_card', 'card_number',
                  'expiry_date', 'card_code', 'payment_day', 'payment_account']


class TestForm(ModelForm):
    name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=254)
    message = forms.CharField(
        max_length=2000,
        widget=forms.Textarea(),
        help_text='Write here your message!'
    )
    source = forms.CharField(       # A hidden input for internal use
        max_length=50,              # tell from which page the user sent the message
        widget=forms.HiddenInput()
    )

    def clean(self):
        cleaned_data = super(TestForm, self).clean()
        name = cleaned_data.get('name')
        email = cleaned_data.get('email')
        message = cleaned_data.get('message')
        if not name and not email and not message:
            raise forms.ValidationError(
                f'name: {name} - email: {email} - message: {message}')

    class Meta:
        model = Test
        fields = '__all__'
