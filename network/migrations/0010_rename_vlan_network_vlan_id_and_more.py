# Generated by Django 4.2.7 on 2023-12-13 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0009_rename_number_vlan_vlan_id_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='network',
            old_name='vlan',
            new_name='vlan_id',
        ),
        migrations.RemoveField(
            model_name='network',
            name='description',
        ),
        migrations.RemoveField(
            model_name='network',
            name='network_address',
        ),
        migrations.RemoveField(
            model_name='network',
            name='network_broadcast',
        ),
        migrations.AddField(
            model_name='network',
            name='nb_hosts',
            field=models.IntegerField(default=0),
        ),
    ]