# Generated by Django 4.2.16 on 2024-11-04 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0007_remove_evenement_is_archived'),
    ]

    operations = [
        migrations.AddField(
            model_name='evenement',
            name='archived',
            field=models.BooleanField(default=False),
        ),
    ]