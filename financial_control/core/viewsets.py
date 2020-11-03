# from rest_framework import status, viewsets
# from rest_framework.response import Response

from .common.viewsets import BaseModelViewSetMultiCreate
from .models import Account, Category, Transaction, Transfer
from .serializers import AccountSerializer, CategorySerializer, TransactionSerializer, TransferSerializer


class AccountViewSet(BaseModelViewSetMultiCreate):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def get_object(self):
        if self.request.method == 'POST':
            obj, created = Account.objects.get_or_create(
                pk=self.kwargs.get('pk'))
            return obj
        else:
            return super(AccountViewSet, self).get_object()


class CategoryViewSet(BaseModelViewSetMultiCreate):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TransactionViewSet(BaseModelViewSetMultiCreate):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


class TransferViewSet(BaseModelViewSetMultiCreate):
    queryset = Transfer.objects.all()
    serializer_class = TransferSerializer
