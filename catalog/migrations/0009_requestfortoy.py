# Generated by Django 4.0.4 on 2022-08-07 12:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalog', '0008_alter_productrequest_requested_toy'),
    ]

    operations = [
        migrations.CreateModel(
            name='RequestforToy',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('notes', models.CharField(help_text='If you have something to add, you can write it here.', max_length=250)),
                ('start_date', models.DateField(help_text='Start date for toy is on ...', null=True, verbose_name='Start Date')),
                ('end_date', models.DateField(help_text='Coming back on ...', null=True, verbose_name='End Date')),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='toyrequestrecipient', to=settings.AUTH_USER_MODEL)),
                ('requested_toy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='toyrequestborrow', to='catalog.toyproduct')),
                ('sender', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('sender_toy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='toyrequestsender', to='catalog.toyproduct')),
            ],
            options={
                'ordering': ['sender', 'sender_toy', 'requested_toy'],
            },
        ),
    ]
