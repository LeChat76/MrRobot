# Generated by Django 4.2.7 on 2023-11-13 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('openclassrooms', '0010_project_project_duration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='skill',
            field=models.ManyToManyField(blank=True, to='openclassrooms.skill'),
        ),
        migrations.AlterField(
            model_name='project',
            name='technology',
            field=models.ManyToManyField(blank=True, to='openclassrooms.technology'),
        ),
    ]
