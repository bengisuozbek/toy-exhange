import re
from django.shortcuts import render, redirect

from datetime import datetime
from price.decorators import unauthenticated_user, allowed_users, admin_only
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

import csv, io
from .models import *
from catalog.forms import CsvModelForm
from catalog.models import *
import csv
# Create your views here.

@allowed_users(allowed_roles=['admin'])
def price_upload(request):
    category = request.GET.get('category')
    categories = Category.objects.all()

    if category == None:
        product_objects = ToyProduct.objects.all()
    else:
        product_objects = ToyProduct.objects.filter(category__name=category)


    form = CsvModelForm()

    if request.method == 'POST':
        form = CsvModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            obj = Csv.objects.get(activated=False)
            with open(obj.file_name.path, 'r') as f:
                reader = csv.reader(f)

                for i, row in enumerate(reader):
                    if i == 0:
                        pass
                    else:
                        row = "".join(row)
                        row = row.replace(";", "*")
                        row = row.split("*")
                        serial_number = row[1]
                        toy_name = row[2]
                        prices1 = row[3]
                        prices2 = row[4]
                        cimridata.objects.create(
                            id = int(row[1]) + 1,
                            serial = serial_number, 
                            name = toy_name,
                            price1 = prices1,
                            price2 = prices2,
                        )
                        # print(row)
                        # print(type(row))
                
                obj.activated = True
                obj.save()
            return redirect('price_upload')
        else:
            print('Form is invalid.')
            return redirect('invalid')

    context = {
        'product_objects': product_objects,
        'categories': categories,
        'form': form
    }

    return render(request, 'for_admin/price_upload.html', context=context)


# @allowed_users(allowed_roles=['admin'])
# def price_upload(request):
#     template = "for_admin/price_upload.html"

#     # prompt = {
#     #     'product': 'Product information must include Sr.No, Name, Price1'
#     # }

#     if request.method == 'GET':
#         return render(request, template)

#     csv_file = request.FILES['file']

#     if not csv_file.name.endswith(".csv"):
#         messages.error(request, 'This is not a csv file.')

#     #data_set = csv_file.read().decode('UTF-8')
#     #io_string = io.StringIO(data_set)

#     #next(io_string) # The first line is skipped
#     csvreader = csv.reader(request.FILES['file'])
#     header = next(csvreader)
#     print(header)
#     rows = []
#     for row in csvreader:
#         rows.append(row)

#         _, created = akakce.objects.update_or_create(
#             serialnumber = row[0],
#             name = row[1],
#             prices1 = row[2],
#         )
#     print(rows)
    

#     #for column in csv.reader(io_string, delimiter=',', quotechar='|'):
#         #print(column[0])
#         #print(column[1])
#         #print(column[2])

#        #Create updated part

#     context = {}

#     return render(request, template, context)