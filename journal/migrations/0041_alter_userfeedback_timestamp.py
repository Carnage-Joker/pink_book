# Generated by Django 5.0.1 on 2024-11-11 02:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("journal", "0040_alter_userfeedback_timestamp"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userfeedback",
            name="timestamp",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 11, 11, 13, 53, 5, 221864)
            ),
        ),
    ]