# Generated by Django 5.0.1 on 2024-07-01 21:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("journal", "0116_alter_habit_timestamp_alter_userfeedback_timestamp"),
    ]

    operations = [
        migrations.AlterField(
            model_name="habit",
            name="timestamp",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 7, 2, 7, 13, 31, 908674)
            ),
        ),
        migrations.AlterField(
            model_name="userfeedback",
            name="timestamp",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 7, 2, 7, 13, 31, 923821)
            ),
        ),
    ]
