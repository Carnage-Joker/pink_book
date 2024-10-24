# Generated by Django 5.0.1 on 2024-10-10 21:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("journal", "0016_alter_userfeedback_timestamp"),
    ]

    operations = [
        migrations.AddField(
            model_name="habit",
            name="longest_streak_days",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="userfeedback",
            name="timestamp",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 10, 11, 8, 47, 31, 794719)
            ),
        ),
    ]
