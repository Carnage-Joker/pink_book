# Generated by Django 5.0.1 on 2024-07-17 22:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("journal", "0005_alter_habit_timestamp_alter_userfeedback_timestamp"),
    ]

    operations = [
        migrations.AlterField(
            model_name="habit",
            name="timestamp",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 7, 18, 8, 58, 24, 617812)
            ),
        ),
        migrations.AlterField(
            model_name="userfeedback",
            name="timestamp",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 7, 18, 8, 58, 24, 617812)
            ),
        ),
    ]
