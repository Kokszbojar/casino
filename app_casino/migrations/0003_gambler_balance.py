# Generated by Django 3.0.3 on 2021-07-21 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_casino', '0002_remove_gambler_balance'),
    ]

    operations = [
        migrations.AddField(
            model_name='gambler',
            name='balance',
            field=models.IntegerField(default=0),
        ),
    ]
