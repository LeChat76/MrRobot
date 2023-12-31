# Generated by Django 4.2.7 on 2023-12-07 09:37

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vlan',
            name='vlan_id',
        ),
        migrations.AlterField(
            model_name='vlan',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False, unique=True, validators=[django.core.validators.RegexValidator(message='Le VLAN ID doit contenir uniquement des entiers positifs.', regex='^[0-9]*$')]),
        ),
    ]
