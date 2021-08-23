# Generated by Django 3.2.4 on 2021-08-06 11:10

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0005_auto_20210805_1215'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='color',
            field=models.CharField(default='Unknown', max_length=50),
        ),
        migrations.AddField(
            model_name='item',
            name='condition',
            field=models.CharField(choices=[('N', 'New'), ('U', 'Used'), ('NS', 'Not Specified')], default='NS', max_length=2),
        ),
        migrations.AddField(
            model_name='saleoffer',
            name='free_delivery',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='saleoffer',
            name='quantity',
            field=models.PositiveIntegerField(default=1, help_text='Please pass the number of pieces in the package.'),
        ),
        migrations.AlterField(
            model_name='saleoffer',
            name='exp_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 5, 11, 10, 30, 832578, tzinfo=utc), editable=False),
        ),
    ]