# Generated by Django 4.0.6 on 2022-07-26 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('borg', '0002_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='label',
            name='visible',
            field=models.BooleanField(default=True),
        ),
    ]
