# Generated by Django 4.2.16 on 2024-11-04 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_alter_evenement_status_publication_archiveevenement'),
    ]

    operations = [
        migrations.AddField(
            model_name='evenement',
            name='is_archived',
            field=models.BooleanField(default=False),
        ),
    ]
