# Generated by Django 5.0.1 on 2024-11-08 21:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("journal", "0038_alter_userfeedback_timestamp"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userfeedback",
            name="timestamp",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 11, 9, 8, 45, 31, 225715)
            ),
        ),
    ]
