# Generated by Django 5.0.4 on 2024-12-12 23:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_evenement', '0002_alter_evenement_disponibilite_event_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evenement',
            name='disponibilite_event',
            field=models.CharField(max_length=128),
        ),
        migrations.AlterField(
            model_name='notifier',
            name='type_notif',
            field=models.CharField(max_length=128),
        ),
        migrations.AlterField(
            model_name='participer',
            name='ticket_virtuel',
            field=models.CharField(max_length=32),
        ),
    ]