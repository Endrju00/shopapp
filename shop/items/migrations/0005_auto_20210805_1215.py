# Generated by Django 3.2.4 on 2021-08-05 10:15

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0004_auto_20210804_1418'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='height',
            field=models.PositiveIntegerField(help_text='Please pass the height in centimeters.'),
        ),
        migrations.AlterField(
            model_name='item',
            name='length',
            field=models.PositiveIntegerField(help_text='Please pass the length in centimeters.'),
        ),
        migrations.AlterField(
            model_name='item',
            name='width',
            field=models.PositiveIntegerField(help_text='Please pass the width in centimeters.'),
        ),
        migrations.AlterField(
            model_name='saleoffer',
            name='exp_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 4, 10, 15, 19, 474000, tzinfo=utc), editable=False),
        ),
    ]
