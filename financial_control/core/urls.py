from django.urls import path, include, register_converter
from rest_framework import routers

from . import views
from .viewsets import AccountViewSet, CategoryViewSet, EntryViewSet
from .url_converter import OptionalIntConverter

router = routers.SimpleRouter()
router.register(r'accounts', AccountViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'entries', EntryViewSet)

register_converter(OptionalIntConverter, 'optional_int')


urlpatterns = [
    path('', views.index, name='index'),
    path('api/', include(router.urls)),

    path('accounts/', views.account_list, name='account_list'),
    path('accounts/new', views.account_new, name='account_new'),
    path('accounts/<int:pk>', views.account_form, name='account_form'),
    path('accounts/<int:pk>/delete', views.account_delete, name='account_delete'),

    path('categories/', views.category_list, name='category_list'),
    path('categories/new', views.category_new, name='category_new'),
    path('categories/<int:pk>', views.category_form, name='category_form'),
    path('categories/<int:pk>/delete',
         views.category_delete, name='category_delete'),

    path('entries/', views.entry_list, name='entry_list'),
    # path('entries/new', views.entry_new, name='entry_new'),
    path('entries/<int:pk>', views.entry_form, name='entry_form'),
    path('entries/<int:pk>/delete', views.entry_delete, name='entry_delete'),
]
