# Generated by Django 3.2.4 on 2021-08-27 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0019_notification_sender_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='sender_id',
            field=models.PositiveIntegerField(),
        ),
    ]
