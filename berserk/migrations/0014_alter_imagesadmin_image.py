# Generated by Django 4.2.5 on 2023-10-01 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('berserk', '0013_alter_imagesadmin_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagesadmin',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='user_images/'),
        ),
    ]