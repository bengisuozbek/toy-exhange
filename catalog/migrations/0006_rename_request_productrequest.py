# Generated by Django 4.0.4 on 2022-08-03 19:13

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalog', '0005_alter_request_sender'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Request',
            new_name='ProductRequest',
        ),
    ]
