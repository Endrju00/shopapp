# Generated by Django 3.2.4 on 2021-08-24 16:08

import datetime
import django.core.validators
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0030_auto_20210824_1759'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='height',
            field=models.FloatField(blank=True, help_text='Please pass the height in meters.', validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='item',
            name='length',
            field=models.FloatField(blank=True, help_text='Please pass the length in meters.', validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='item',
            name='weight',
            field=models.FloatField(blank=True, help_text='Please pass the weight in kilograms.', validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='item',
            name='width',
            field=models.FloatField(blank=True, help_text='Please pass the width in meters.', validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='saleoffer',
            name='exp_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 23, 16, 8, 30, 377925, tzinfo=utc), editable=False),
        ),
    ]
