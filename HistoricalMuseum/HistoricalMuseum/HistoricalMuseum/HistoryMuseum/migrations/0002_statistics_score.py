# Generated by Django 3.0.8 on 2020-09-25 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HistoryMuseum', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='statistics',
            name='score',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
