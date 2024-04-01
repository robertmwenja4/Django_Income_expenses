from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Expense
from django.contrib import messages
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from userpreferences.models import UserPreference

# Create your views here.
@login_required(login_url="/authentication/login")
def index(request):
    categories = Category.objects.all()
    expenses = Expense.objects.filter(owner= request.user)
    paginator = Paginator(expenses, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    currency = UserPreference.objects.get(user=request.user).currency
    # currency = "USD"
    
    context = {
        'categories' : categories,
        'expenses' : expenses,
        'page_obj': page_obj,
        'currency' : currency
    }
    return render(request, 'expenses/index.html', context=context)
@login_required(login_url="/authentication/login")
def add_expenses(request):
    categories = Category.objects.all()
    context = {
        'categories' : categories,
        'values' : request.POST,
    }

    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['date']
        category = request.POST['category']
        if not amount:
            messages.error(request, 'Amount is Required')
            return render(request, 'expenses/add_expenses.html', context )
        if not description:
            messages.error(request, 'Description is Required')
            return render(request, 'expenses/add_expenses.html', context )
        Expense.objects.create(owner=request.user, amount=amount,
                               description=description, date=date, category=category)
        messages.success(request, 'Expense Saved Successfully')
        return redirect('expenses')
    return render(request, 'expenses/add_expenses.html', context=context )

def expense_edit(request, id):
    expense = Expense.objects.get(pk=id)
    categories = Category.objects.all()
    context = {
        'expense' : expense,
        'values' : expense,
        'categories' : categories
    }
    if request.method == 'GET':
        
        return render(request, 'expenses/edit-expense.html', context)
    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['date']
        category = request.POST['category']
        if not amount:
            messages.error(request, 'Amount is Required')
            return render(request, 'expenses/edit-expense.html', context )
        if not description:
            messages.error(request, 'Description is Required')
            return render(request, 'expenses/edit-expense.html', context )
        expense.owner=request.user
        expense.amount=amount
        expense.date=date
        expense.description=description
        expense.category=category
        expense.save()
        messages.success(request, 'Expense Updated Successfully')
        return render(request, 'expenses/edit-expense.html', context)
    
def delete_expense(request, id):
    expense = Expense.objects.get(pk=id)
    # import pdb
    # pdb.set_trace()
    expense.delete()
    messages.success(request, "Expense Deleted Successfully!!")
    return redirect('expenses')
            
def search(request):
    if request.method == 'POST':
        search_text = json.loads(request.body).get('searchText')
        expenses = Expense.objects.filter(amount__istartswith=search_text,
                                          owner=request.user) | Expense.objects.filter(date__istartswith=search_text,
                                            owner=request.user) | Expense.objects.filter(description__icontains=search_text,
                                                                                         owner=request.user) | Expense.objects.filter(category__icontains=search_text, owner=request.user)
        data = expenses.values()
        return JsonResponse(list(data), safe=False)
