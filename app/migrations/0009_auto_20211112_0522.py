# Generated by Django 3.2.8 on 2021-11-12 04:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_alter_user_following'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='height',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='width',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(height_field='height', upload_to='post/', width_field='width'),
        ),
    ]
