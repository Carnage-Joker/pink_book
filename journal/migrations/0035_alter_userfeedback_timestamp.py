# Generated by Django 5.0.1 on 2024-08-09 03:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("journal", "0034_faq_alter_userfeedback_timestamp"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userfeedback",
            name="timestamp",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 8, 9, 13, 3, 23, 135703)
            ),
        ),
    ]
