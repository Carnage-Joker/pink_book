# Generated by Django 5.0.1 on 2024-08-07 14:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("journal", "0024_customuser_is_moderator_alter_userfeedback_timestamp"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userfeedback",
            name="timestamp",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 8, 8, 0, 51, 17, 353601)
            ),
        ),
    ]