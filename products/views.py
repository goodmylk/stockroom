from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Batch, Product
from django.utils import timezone


products = Product.objects

@login_required(login_url="/accounts/login")
def addbatch(request):
    if request.method == 'POST':
        if request.POST['product'] and request.POST['batch'] and request.POST['qnt']:
            batch = Batch()
            batch.batch_number = request.POST['batch']
            batch.quantity = request.POST['qnt']
            batch.current_stock = request.POST['qnt']
            batch.submitted_by = request.user
            batch.productname = Product.objects.get(id=request.POST['product'])
            if request.POST['date']:
                batch.manufacture_date = request.POST['date']
            else:
                batch.manufacture_date = timezone.datetime.now()

            if request.POST['comments']:
                batch.comments = request.POST['comments']

            batch.save()
            msg = {}
            msg['message'] = 'Batch added successfully.'
            return render(request, 'batch/addbatch.html', {'message':msg, 'products':products})
        else:
            return render(request, 'batch/addbatch.html',{'error':'Product, Batch Number and Quantity are required.','products':products})
    else:
        return render(request, 'batch/addbatch.html', {'products':products})
