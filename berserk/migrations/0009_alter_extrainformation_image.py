# Generated by Django 4.2.5 on 2023-09-25 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('berserk', '0008_alter_serarchrecord_value'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extrainformation',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='user_images/'),
        ),
    ]
