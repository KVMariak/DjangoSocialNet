# Generated by Django 3.1.4 on 2020-12-29 01:41

from django.db import migrations, models
import publications.models


class Migration(migrations.Migration):

    dependencies = [
        ('publications', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(null=True, upload_to=publications.models.upload_location),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
