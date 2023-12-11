# Generated by Django 4.2.7 on 2023-12-11 09:29

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('network', '0008_alter_vlan_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vlan',
            old_name='number',
            new_name='vlan_id',
        ),
        migrations.AlterUniqueTogether(
            name='vlan',
            unique_together={('user', 'vlan_id')},
        ),
    ]
