# Generated by Django 4.2.5 on 2023-09-23 15:10

import berserk.validators.validator_password
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('berserk', '0003_advuser_password1_alter_advuser_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='advuser',
            name='password1',
        ),
        migrations.AlterField(
            model_name='advuser',
            name='password',
            field=models.CharField(blank=True, max_length=25, null=True, validators=[berserk.validators.validator_password.Validator_passwod]),
        ),
    ]