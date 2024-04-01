from django.shortcuts import render, redirect, get_object_or_404
from .models import Source, UserIncome
from django.core.paginator import Paginator
from userpreferences.models import UserPreference
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse

# Create your views here.
@login_required(login_url="/authentication/login")
def index(request):
    sources = Source.objects.all()
    incomes = UserIncome.objects.filter(owner= request.user)
    paginator = Paginator(incomes, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    currency = UserPreference.objects.get(user=request.user).currency
    # currency = "USD"
    
    context = {
        'sources' : sources,
        'incomes' : incomes,
        'page_obj': page_obj,
        'currency' : currency
    }
    return render(request, 'income/index.html', context=context)

@login_required(login_url="/authentication/login")
def add_income(request):
    sources = Source.objects.all()
    context = {
        'sources' : sources,
        'values' : request.POST,
    }

    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['date']
        sources = request.POST['source']
        if not amount:
            messages.error(request, 'Amount is Required')
            return render(request, 'income/add_income.html', context )
        if not description:
            messages.error(request, 'Description is Required')
            return render(request, 'income/add_income.html', context )
        UserIncome.objects.create(owner=request.user, amount=amount,
                               description=description, date=date, source=sources)
        messages.success(request, 'UserIncome Saved Successfully')
        return redirect('income')
    return render(request, 'income/add_income.html', context=context )

def income_edit(request, id):
    income = UserIncome.objects.get(pk=id)
    sources = Source.objects.all()
    context = {
        'income' : income,
        'values' : income,
        'sources' : sources
    }
    if request.method == 'GET':
        
        return render(request, 'income/edit-income.html', context)
    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['date']
        source = request.POST['source']
        if not amount:
            messages.error(request, 'Amount is Required')
            return render(request, 'income/edit-income.html', context )
        if not description:
            messages.error(request, 'Description is Required')
            return render(request, 'income/edit-income.html', context )
        income.owner=request.user
        income.amount=amount
        income.date=date
        income.description=description
        income.source=source
        income.save()
        messages.success(request, 'Income Updated Successfully')
        # return render(request, 'income/edit-income.html', context)
        return redirect('income')
    
def delete_income(request, id):
    income = UserIncome.objects.get(pk=id)
    # import pdb
    # pdb.set_trace()
    income.delete()
    messages.success(request, "Income Deleted Successfully!!")
    return redirect('income')

def search(request):
    if request.method == 'POST':
        search_text = json.loads(request.body).get('searchText')
        incomes = UserIncome.objects.filter(amount__istartswith=search_text,
                                          owner=request.user) | UserIncome.objects.filter(date__istartswith=search_text,
                                            owner=request.user) | UserIncome.objects.filter(description__icontains=search_text,
                                                                                         owner=request.user) | UserIncome.objects.filter(source__icontains=search_text, owner=request.user)
        data = incomes.values()
        return JsonResponse(list(data), safe=False)