# Generated by Django 4.0.4 on 2022-08-07 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0011_alter_person_profile_pic_alter_toyproduct_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='profile_pic',
            field=models.ImageField(blank=True, default='profile.png', null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='toyproduct',
            name='image',
            field=models.ImageField(blank=True, default='imageicon.png', null=True, upload_to=''),
        ),
    ]
