# Generated by Django 3.2.4 on 2021-08-06 17:16

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0006_auto_20210806_1310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='saleoffer',
            name='exp_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 5, 17, 16, 27, 177739, tzinfo=utc), editable=False),
        ),
    ]