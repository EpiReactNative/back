# Generated by Django 3.2.8 on 2021-10-26 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='data',
            field=models.TextField(blank=True),
        ),
    ]