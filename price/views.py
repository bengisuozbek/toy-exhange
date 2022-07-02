from django.shortcuts import render, redirect

from datetime import datetime
from price.decorators import unauthenticated_user, allowed_users, admin_only
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

import csv, io
from .models import akakce
# Create your views here.

@allowed_users(allowed_roles=['admin'])
def price_upload(request):
    template = "for_admin/price_upload.html"

    prompt = {
        'product': 'Product information must include Sr.No, Name, Price1'
    }

    if request.method == 'GET':
        return render(request, template, prompt)

    csv_file = request.FILES['file']

    if not csv_file.name.endswith(".csv"):
        messages.error(request, 'This is not a csv file.')

    #data_set = csv_file.read().decode('UTF-8')
    #io_string = io.StringIO(data_set)

    #next(io_string) # The first line is skipped

    csvreader = csv.reader(request.FILES['file'])
    header = next(csvreader)
    print(header)
    rows = []
    for row in csvreader:
        rows.append(row)

        _, created = akakce.objects.update_or_create(
            serial_number = row[0],
            name = row[1],
            prices1 = row[2],
        )
    print(rows)
    

    #for column in csv.reader(io_string, delimiter=',', quotechar='|'):
        #print(column[0])
        #print(column[1])
        #print(column[2])

       #Create updated part

    context = {}

    return render(request, template, context)