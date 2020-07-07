from django.urls import path, include, register_converter, re_path
from rest_framework import routers

from . import views
from . import api_views
from .viewsets import AccountViewSet, CategoryViewSet, TransactionViewSet
from .url_converter import OptionalIntConverter

router = routers.SimpleRouter()
router.register(r'accounts', AccountViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'transactions', TransactionViewSet)

register_converter(OptionalIntConverter, 'optional_int')


urlpatterns = [
    path('', views.index),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('process_balance/', views.process_balance, name='process_balance'),
    path('api/', include(router.urls)),
    re_path('api/accounts_statment/$', api_views.accounts_statment,
            name='api_accounts_statment'),

    path('accounts/', views.account_list, name='account_list'),
    path('accounts/new', views.account_new, name='account_new'),
    path('accounts/<int:pk>', views.account_form, name='account_form'),
    path('accounts/<int:pk>/delete', views.account_delete, name='account_delete'),

    path('categories/', views.category_list, name='category_list'),
    path('categories/new', views.category_new, name='category_new'),
    path('categories/<int:pk>', views.category_form, name='category_form'),
    path('categories/<int:pk>/delete',
         views.category_delete, name='category_delete'),

    path('transactions/', views.transaction_list, name='transaction_list'),
    re_path('transactions/new/$', views.transaction_new, name='transaction_new'),
    path('transactions/<int:pk>', views.transaction_form, name='transaction_form'),
    path('transactions/<int:pk>/delete',
         views.transaction_delete, name='transaction_delete'),

    path('transfers/', views.transfer_list, name='transfer_list'),
    re_path('transfers/new/$', views.transfer_new, name='transfer_new'),
    path('transfers/<int:pk>', views.transfer_form, name='transfer_form'),
    path('transfers/<int:pk>/delete',
         views.transfer_delete, name='transfer_delete'),

    path('programed_transactions/', views.programed_transaction_list,
         name='programed_transaction_list'),
    path('programed_transactions/new',
         views.programed_transaction_new, name='programed_transaction_new'),
    path('programed_transactions/<int:pk>',
         views.programed_transaction_form, name='programed_transaction_form'),
    path('programed_transactions/<int:pk>/delete',
         views.programed_transaction_delete, name='programed_transaction_delete'),
]
