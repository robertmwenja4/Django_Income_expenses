from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.index, name='expenses'),
    path('add-expenses', views.add_expenses, name='add-expenses'),
    path('edit-expense/<id>', views.expense_edit, name='edit-expense'),
    path('expense-delete/<id>', views.delete_expense, name='expense-delete'),
    path('search-expenses', csrf_exempt(views.search), name='search-expenses')
]
