from django.urls import path, include
from rest_framework import routers

from . import views
from .viewsets import AccountViewSet, CategoryViewSet, EntryViewSet

router = routers.SimpleRouter()
router.register(r'accounts', AccountViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'entries', EntryViewSet)


urlpatterns = [
    path('', views.index, name='index'),
    path('api/', include(router.urls)),

    path('accounts/', views.account_list, name='account_list'),
    path('accounts/<int:pk>', views.account_form, name='account_form'),

    path('categories/', views.category_list, name='category_list'),
    path('categories/<int:pk>', views.category_form, name='category_form'),

    path('entries/', views.entry_list, name='entry_list'),
    path('entries/<int:pk>', views.entry_form, name='entry_form'),
]
