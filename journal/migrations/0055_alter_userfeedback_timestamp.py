# Generated by Django 5.0.1 on 2024-10-01 08:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("journal", "0054_alter_userfeedback_timestamp"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userfeedback",
            name="timestamp",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 10, 1, 18, 19, 13, 796319)
            ),
        ),
    ]
