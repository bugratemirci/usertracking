# Generated by Django 4.2.4 on 2023-09-01 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='photo_path',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
