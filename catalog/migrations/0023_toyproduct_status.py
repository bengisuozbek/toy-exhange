# Generated by Django 4.0.4 on 2022-08-14 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0022_datafromcimri_price1'),
    ]

    operations = [
        migrations.AddField(
            model_name='toyproduct',
            name='status',
            field=models.CharField(default='Available', max_length=20),
        ),
    ]
