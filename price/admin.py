from django.contrib import admin

# Register your models here.
from django.contrib import admin

# Register your models here.
from .models import *
                                  
@admin.register(akakce)
class RequestofToyAdmin(admin.ModelAdmin):
    list_display = ('date', 'serial_number', 'name', 'prices1')
