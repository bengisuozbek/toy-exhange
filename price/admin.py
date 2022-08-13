from django.contrib import admin

# Register your models here.
from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(cimri)
admin.site.register(cimridata)

@admin.register(cimritoy)
class RequestofToyAdmin(admin.ModelAdmin):
    list_display = ('date', 'serial', 'name', 'price1', 'price2')

@admin.register(toyfromcimri)
class RequestofToyAdmin(admin.ModelAdmin):
    list_display = ('date', 'serial', 'name', 'price1', 'price2')
