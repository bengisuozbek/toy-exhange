# Generated by Django 4.0.4 on 2022-05-15 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_delete_toyprices_akakce'),
    ]

    operations = [
        migrations.CreateModel(
            name='akakce',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now=True)),
                ('serial_number', models.IntegerField(verbose_name='Sr.No')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('prices1', models.CharField(max_length=255, verbose_name='Prices1')),
            ],
        ),
    ]
