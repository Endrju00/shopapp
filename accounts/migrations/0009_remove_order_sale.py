# Generated by Django 3.2.4 on 2021-08-23 10:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_rename_profile_order_buyer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='sale',
        ),
    ]
