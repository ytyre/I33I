# Generated by Django 4.2.5 on 2023-09-23 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('berserk', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advuser',
            name='username',
            field=models.TextField(blank=True, max_length=33, null=True, unique=True, verbose_name='Username'),
        ),
    ]
