# Generated by Django 5.0.1 on 2024-11-13 00:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("journal", "0048_alter_userfeedback_timestamp"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userfeedback",
            name="timestamp",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 11, 13, 11, 45, 47, 441649)
            ),
        ),
    ]
