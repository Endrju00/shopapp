# Generated by Django 3.2.4 on 2021-08-04 12:18

import datetime
from django.db import migrations, models
from django.utils.timezone import utc
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0003_rename_product_name_item_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='saleoffer',
            name='exp_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 3, 12, 18, 50, 767983, tzinfo=utc), editable=False),
        ),
        migrations.AddField(
            model_name='saleoffer',
            name='pub_date',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
    ]
