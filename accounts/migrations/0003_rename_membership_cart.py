# Generated by Django 3.2.4 on 2021-08-18 10:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0018_alter_saleoffer_exp_date'),
        ('accounts', '0002_auto_20210818_1241'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Membership',
            new_name='Cart',
        ),
    ]
