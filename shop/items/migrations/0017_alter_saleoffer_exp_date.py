# Generated by Django 3.2.4 on 2021-08-18 10:41

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0016_auto_20210816_0955'),
    ]

    operations = [
        migrations.AlterField(
            model_name='saleoffer',
            name='exp_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 17, 10, 41, 21, 441143, tzinfo=utc), editable=False),
        ),
    ]
