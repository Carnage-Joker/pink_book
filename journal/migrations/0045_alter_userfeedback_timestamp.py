# Generated by Django 5.0.1 on 2024-11-12 22:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("journal", "0044_alter_userfeedback_timestamp"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userfeedback",
            name="timestamp",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 11, 13, 9, 30, 24, 543849)
            ),
        ),
    ]
