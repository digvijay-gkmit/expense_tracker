# Generated by Django 5.1.4 on 2024-12-26 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='mobile_no',
            field=models.CharField(blank=True, max_length=13, null=True),
        ),
    ]