# Generated by Django 3.0.3 on 2021-07-22 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_casino', '0003_gambler_balance'),
    ]

    operations = [
        migrations.CreateModel(
            name='CoinBet',
            fields=[
                ('heads_bet', models.IntegerField()),
                ('tails_bet', models.IntegerField()),
                ('name', models.IntegerField(primary_key=True, serialize=False)),
            ],
        ),
    ]
