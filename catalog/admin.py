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
                            
@admin.register(ToyProduct)
class ToyProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'brand', 'age', 'display_category')


@admin.register(RequestforToy)
class ToyProductAdmin(admin.ModelAdmin):
    list_display = ('sender', 'sender_toy', 'requested_toy', 'notes', 'start_date', 'end_date')