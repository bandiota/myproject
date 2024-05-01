from django.shortcuts import render, redirect
from.models import *
from.forms import *
from django.http import HttpResponse
import csv
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import datetime


# def home (request):
#     title = 'Stock Management'
#     context = {'title' : title}
#     return render(request, "stockmgmgt/home.html", context)



def home (request):
    title = 'Stock Management'
    context = {
        'title' : title
    }
    # return render(request, "home.html", context)
    return redirect('list_items')

@login_required
def list_items(request):
    header   =   'LIST OF ITEMS'
    form = StockSearchForm(request.POST or None)
    queryset   =   Stock.objects.all()
    context = {
            'header'  :   header,
            'form'    :   form,
            'queryset': queryset
        }
    
    if request.method=='POST':
        category = form['category'].value()
        queryset = Stock.objects.filter(
            item_name__icontains=form['item_name'].value(),
            )
        if (category != ""):
            queryset = queryset.filter(category_id=category)
        
        
        if form['export_to_CSV'].value() == True:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="List of stock.csv"'
            writer = csv.writer(response)
            writer.writerow(['CATEGORY', 'ITEM NAME', 'QUANTITY', 'UNIT'])
            instance = queryset
            for stock in instance:
                writer.writerow([stock.category, stock.item_name, stock.quantity, stock.unit])
            return response

        context = {
            'header'  :   header,
            'form'    :   form,
            'queryset': queryset
        }
    return render (request, 'stockmgmgt/list_items.html', context)


@login_required
def add_items(request):
    form = StockCreateForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Item added successfully!")
        return redirect ('list_items')
    context = {
            'form' : form,
            'title' : 'Add Items'
        }
    return render(request, 'stockmgmgt/add_items.html', context)

@login_required
def update_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = StockUpdateForm(instance=queryset)
    if request.method == 'POST':
        form = StockUpdateForm(request.POST, instance=queryset)
        if form.is_valid():
            form.save()
            messages.success(request, "Item updated Successfully!")
            return redirect('list_items')

    context ={
            "form" : form,
            "title": "Edit Item",
        }
    return render(request,'stockmgmgt/add_items.html',context)


@login_required
def delete_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    if request.method=='POST':
        queryset.delete()
        messages.success(request,"Item has been deleted")
        return redirect('list_items')
    context = {'title': 'DELETE ITEM'}
    return render(request,'stockmgmgt/delete_items.html',context)

@login_required
def stock_detail(request, pk):
    queryset = Stock.objects.get(id=pk)
    context = {
        "title": queryset.item_name,
        'queryset': queryset
        }
    return render(request,'stockmgmgt/stock_detail.html',context)

@login_required
def issue_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = IssueForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.receive_quantity = 0
        instance.quantity -= instance.issue_quantity
        instance.issue_by = str(request.user)
        messages.success(request, "Issued Succesfull. " + str(instance.quantity) + " " + str(instance.item_name) + "s now left in Store" )
        instance.save()
        # issue_history = StockHistory (
        #     id = instance.id,
        #     last_updated = instance.last_updated,
        #     category_id = instance.category_id,
        #     item_name = instance.item_name,
        #     quantity = instance.quantity,
        #     issue_to = instance.issue_to,
        #     issue_by = instance.issue_by,
        #     issue_quantity = instance.issue_quantity,
        # )
        # issue_history.save()
        return redirect('/stock/stock_detail/'+str(instance.id))
    context = {
        'title': 'Issue ' + str(queryset.item_name),
        'queryset' : queryset,
        'form': form,
        'username': 'Issue By: ' + str(request.user),
    }
    return render (request, 'stockmgmgt/add_items.html', context)

@login_required
def receive_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = ReceiveForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.issue_quantity = 0
        instance.quantity += instance.receive_quantity
        instance.receive_by = str(request.user)
        instance.save()
        # receive_history = StockHistory (
        #     id = instance.id,
        #     last_updated = instance.last_updated,
        #     category_id = instance.category_id,
        #     item_name = instance.item_name,
        #     quantity = instance.quantity,
        #     receive_quantity = instance.receive_quantity,
        #     receive_by = instance.receive_by,
        # )
        # receive_history.save()
        messages.success(request, "Received Successfully " + str(instance.receive_quantity) +" "+ str(instance.item_name) + "s now in Store")
        return redirect ('/stock/stock_detail/' + str(instance.id))
    context  ={
        'title':'Receive '+ str(queryset.item_name),
        'instance':queryset,
        'form':form,
        'username': 'Receive By: ' + str(request.user),
    }
    return render(request,"stockmgmgt/add_items.html", context)

@login_required
def reorder_level(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = ReorderLevelForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save (commit=False)
        instance.save()
        messages.success(request, "Reorder Level for " + str(instance.item_name)+" is updated to " + str(instance.reorder_level))
        return redirect ('list_items')
    context={
        "title": "Reorder Level for",
        "instance" : queryset,
        "form" : form,
    }
    return render(request,'stockmgmgt/add_items.html', context)


@login_required
def list_history(request):
    header = 'HISTORY DATA'
    queryset = StockHistory.objects.all()
    form = StockHistorySearchForm(request.POST  or None)
    context = {
        'header':header,
        'queryset':queryset,
        'form': form,
    }
    
    if request.method == 'POST':
        category = form['category'].value()
        queryset = StockHistory.objects.filter(
								item_name__icontains=form['item_name'].value(),
								last_updated__range=[
													form['start_date'].value(),
													form['end_date'].value()
													]
								)


        if (category != ""):
            queryset = queryset.filter(category_id=category)

        if form['export_to_CSV'].value() == True:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="Stock History.csv"'
            writer = csv.writer(response)
            writer.writerow(
				['CATEGORY', 
				'ITEM NAME',
				'QUANTITY', 
				'ISSUE QUANTITY', 
				'RECEIVE QUANTITY', 
				'RECEIVE BY', 
				'ISSUE BY', 
				'LAST UPDATED'])
            instance = queryset
            for stock in instance:
                writer.writerow(
				[stock.category, 
				stock.item_name, 
				stock.quantity, 
				stock.issue_quantity, 
				stock.receive_quantity, 
				stock.receive_by, 
				stock.issue_by, 
				stock.last_updated])
            return response
            
        context = {
            'form': form,
            'header': header,
            'queryset' : queryset
        }
    return render (request, 'stockmgmgt/list_history.html',context)

@login_required
def add_category(request):
    form = CategoryCreationForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Category created successfully!")
        return redirect ('list_items')
    context = {
            'form' : form,
            'title' : 'Add Category'
        }
    return render(request, 'stockmgmgt/add_category.html', context)

@login_required
def view_category(request):
    queryset = Category.objects.all()
    context = {
        'title' : 'View Categories',
        'queryset' : queryset
    }
    return render (request, 'stockmgmgt/view_category.html', context)

@login_required
def update_category(request, pk):
    queryset = Category.objects.get(id=pk)
    form = CategoryUpdateForm(instance=queryset)
    if request.method == 'POST':
        form = CategoryUpdateForm(request.POST, instance=queryset)
        if form.is_valid():
            form.save()
            messages.success(request, "Category updated Successfully!")
            return redirect('view_category')
    context ={
            "form" : form,
            "title": "Update Category",
        }
    return render(request,'stockmgmgt/update_category.html',context)


@login_required
def delete_category(request, pk):
    queryset = Category.objects.get(id=pk)
    if request.method=='POST':
        queryset.delete()
        messages.success(request,"Item has been deleted")
        return redirect('view_category')
    context = {'title': 'DELETE CATEGORY'}
    return render(request,'stockmgmgt/delete_category.html',context)
