from django.urls import path, re_path
from .import views
from .views import *
from django.contrib import admin
from django.views.static import serve

urlpatterns = [
    #path('', invoices, name='invoices'),
    #path('invoice/<int:invoice_id>/', invoice_view, name='invoice_view'),
   # path('invoices/create/', create_invoice, name='create_invoice'),
]

