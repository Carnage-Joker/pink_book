# Generated by Django 5.0.1 on 2024-10-09 14:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("journal", "0011_alter_userfeedback_timestamp"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userfeedback",
            name="timestamp",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 10, 10, 1, 56, 4, 40116)
            ),
        ),
    ]