# Generated by Django 5.0.1 on 2024-10-06 23:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("journal", "0007_alter_userfeedback_timestamp"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="subscription_tier",
            field=models.CharField(default="free", max_length=50),
        ),
        migrations.AlterField(
            model_name="userfeedback",
            name="timestamp",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 10, 7, 10, 51, 10, 908266)
            ),
        ),
    ]
