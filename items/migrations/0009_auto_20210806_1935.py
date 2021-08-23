# Generated by Django 3.2.4 on 2021-08-06 17:35

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0008_auto_20210806_1925'),
    ]

    operations = [
        migrations.AddField(
            model_name='saleoffer',
            name='title',
            field=models.CharField(default=None, max_length=20),
        ),
        migrations.AlterField(
            model_name='saleoffer',
            name='exp_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 5, 17, 35, 32, 919948, tzinfo=utc), editable=False),
        ),
    ]