# Generated by Django 3.0.3 on 2021-08-06 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_casino', '0006_auto_20210804_0019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gambler',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]