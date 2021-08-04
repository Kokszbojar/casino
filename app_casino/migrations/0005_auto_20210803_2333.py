# Generated by Django 3.0.3 on 2021-08-03 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_casino', '0004_coinbet'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=2000)),
                ('user', models.IntegerField(default=0)),
            ],
        ),
        migrations.AlterField(
            model_name='gambler',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]