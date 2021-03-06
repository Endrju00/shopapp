# Generated by Django 3.2.4 on 2021-08-28 15:15

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0043_alter_saleoffer_exp_date'),
        ('accounts', '0023_mark'),
    ]

    operations = [
        migrations.AddField(
            model_name='mark',
            name='sale',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='items.saleoffer'),
        ),
        migrations.AddField(
            model_name='mark',
            name='text',
            field=models.TextField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='mark',
            name='value',
            field=models.FloatField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)]),
        ),
    ]
