# Generated by Django 5.0.1 on 2024-07-25 02:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("journal", "0019_task_alter_habit_timestamp_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="points",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="habit",
            name="timestamp",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 7, 25, 12, 34, 59, 456542)
            ),
        ),
        migrations.AlterField(
            model_name="userfeedback",
            name="timestamp",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 7, 25, 12, 34, 59, 465070)
            ),
        ),
    ]
