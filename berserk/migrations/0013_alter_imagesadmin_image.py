# Generated by Django 4.2.5 on 2023-09-30 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('berserk', '0012_imagesadmin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagesadmin',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
