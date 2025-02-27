from django.db import models
from django.utils.translation import gettext as _
# Create your models here.

# BRAND WILL BE ADDED!!!
# class akakce(models.Model):
#     date = models.DateTimeField(auto_now=True)
#     serial_number = models.IntegerField()

#     name = models.CharField(max_length = 50)
#     prices1 = models.CharField(max_length = 50)

#     def __str__(self):
#         return f'{self.name}'

class cimri(models.Model):
    name = models.CharField(max_length=255)
    price1 = models.CharField(max_length=255)
    price2 = models.CharField(max_length=255)
    serial = models.CharField(max_length=255)

    def __str__(self):
        """String for representing the Model object."""
        return f"{self.name}-{self.serial}"

class cimridata(models.Model):
    name = models.CharField(max_length=255)
    price1 = models.CharField(max_length=255)
    price2 = models.CharField(max_length=255)
    serial = models.CharField(max_length=255)

    def __str__(self):
        """String for representing the Model object."""
        return str(self.name)
