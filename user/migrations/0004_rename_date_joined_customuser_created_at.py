# Generated by Django 5.1.4 on 2024-12-23 07:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_remove_customuser_is_verified'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='date_joined',
            new_name='created_at',
        ),
    ]