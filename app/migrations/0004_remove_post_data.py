# Generated by Django 3.2.8 on 2021-10-26 10:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_post_data'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='data',
        ),
    ]
