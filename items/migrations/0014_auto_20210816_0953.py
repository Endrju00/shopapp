# Generated by Django 3.2.4 on 2021-08-16 07:53

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('items', '0013_alter_saleoffer_exp_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='saleoffer',
            name='dealer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='saleoffer',
            name='exp_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 15, 7, 53, 24, 960139, tzinfo=utc), editable=False),
        ),
    ]
