# Generated by Django 3.2.4 on 2021-08-27 10:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0021_notification_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notification',
            old_name='status',
            new_name='type',
        ),
    ]
