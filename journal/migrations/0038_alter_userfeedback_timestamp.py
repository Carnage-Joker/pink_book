# Generated by Django 5.0.1 on 2024-11-08 08:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("journal", "0037_alter_customuser_subscription_tier_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userfeedback",
            name="timestamp",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 11, 8, 19, 24, 45, 990624)
            ),
        ),
    ]
