"""Alicia URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from pages.views import (IndexView)
from transactions.views import (TransactionDayView, TransactionCalendarView, TransactionCreateView, TransactionDeleteProduct, TransactionDeleteAllProduct, TransactionEditView, TransactionListView, TransactionDetailView, TransactionDeleteView)
from products.views import (ProductDeleteView, ProductEditView, ProductCreateView)
from clients.views import (ClientCreateView, ClientDeleteView, ClientDetailView, ClientListView, ClientUpdateView)
from bills.views import generate_PDF

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')), # new

    path('product/<int:pk>/delete/', ProductDeleteView.as_view() , name='product_delete'),
    path('product/<int:pk>/edit/', ProductEditView.as_view() , name='product_edit'),
    path('transaction/<int:pk>/product/create/', ProductCreateView.as_view() , name='product_create'),

    path('', IndexView.as_view(), name='index'),
    path('transaction/<int:pk>/', TransactionDetailView.as_view(), name='transaction_detail'),
    path('transaction/<int:pk>/bill/',generate_PDF, name='transaction_bill'),

    path('transaction/<int:pk>/delete/', TransactionDeleteView.as_view(), name='transaction_delete'),
    path('transaction/create/', TransactionCreateView.as_view(), name='transaction_create'),
    path('transaction/create/<int:pk>/', TransactionCreateView.as_view() , name='transaction_create'),
    path('transaction/<int:pk>/edit/', TransactionEditView.as_view() , name='transaction_edit'),
    path('transaction/list/<date>', TransactionDayView.as_view() , name='transaction_day'),
    path('transaction/day/', TransactionListView.as_view() , name='transaction_list'),

    path('transaction/calendar/', TransactionCalendarView.as_view() , name='transaction_calendar'),

    path('transaction/product/<int:pk>/delete/', TransactionDeleteProduct.as_view() , name='product_tmp_delete'),
    path('transaction/product/delete/', TransactionDeleteAllProduct.as_view() , name='product_tmp_delete_all'),

    path('client/list/<int:pk>/create/', ClientCreateView.as_view(),  name='client_create'),
    path('client/list/', ClientListView.as_view(), name='client_list'),
    path('client/list/<int:pk>/edit/', ClientUpdateView.as_view(), name='client_edit'),
    path('client/list/<int:pk>/delete/', ClientDeleteView.as_view(), name='client_delete'),
    path('client/<int:pk>/', ClientDetailView.as_view(), name='client_detail'),
]
