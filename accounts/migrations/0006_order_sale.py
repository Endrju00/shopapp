# Generated by Django 3.2.4 on 2021-08-22 20:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0022_alter_saleoffer_exp_date'),
        ('accounts', '0005_auto_20210822_2213'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='sale',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='items.saleoffer'),
        ),
    ]
