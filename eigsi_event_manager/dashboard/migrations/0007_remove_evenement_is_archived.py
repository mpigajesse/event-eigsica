# Generated by Django 4.2.16 on 2024-11-04 18:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0006_evenement_is_archived'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='evenement',
            name='is_archived',
        ),
    ]
