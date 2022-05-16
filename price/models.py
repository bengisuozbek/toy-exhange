from django.db import models

# Create your models here.

# BRAND WILL BE ADDED!!!
class akakce(models.Model):
    date = models.DateTimeField(auto_now=True)
    serial_number = models.IntegerField()
    name = models.CharField(max_length = 50)
    prices1 = models.FloatField()

    def __str__(self):
        return f'{self.name}'