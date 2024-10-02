# Generated by Django 5.0.1 on 2024-08-11 06:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("journal", "0039_habit_date_alter_userfeedback_timestamp"),
    ]

    operations = [
        migrations.AlterField(
            model_name="billing",
            name="is_active",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="userfeedback",
            name="timestamp",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 8, 11, 16, 2, 18, 849764)
            ),
        ),
    ]