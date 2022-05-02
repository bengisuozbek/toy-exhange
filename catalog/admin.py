from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(AgeInterval)
admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Contact)
#admin.site.register(ToyRequest)
#admin.site.register(ToyRequestList)
#admin.site.register(ToyProduct)

# Define the admin class
class PersonAdmin(admin.ModelAdmin):
    list_display = ('id', 'last_name', 'first_name', 'email')

# Register the admin class with the associated model
admin.site.register(Person, PersonAdmin)   
                                  
@admin.register(ToyRequest)
class RequestofToyAdmin(admin.ModelAdmin):
    list_display = ('toy', 'sender', 'sender_toy', 'notes')


@admin.register(ToyRequestList)
class ToyRequestListAdmin(admin.ModelAdmin):
    list_filter = ['owner', 'toy_from_owner', 'toy_from_borrower']
    list_display = ['owner', 'toy_from_owner', 'display_borrower', 'toy_from_borrower']
    search_fields = ['toy_from_owner__username', 'toy_from_borrower__username']

@admin.register(ToyProduct)
class ToyProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'brand', 'age', 'display_category')