# Generated by Django 4.0.4 on 2022-08-13 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0016_datafromcimri'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datafromcimri',
            name='price1',
            field=models.CharField(max_length=255),
        ),
    ]
