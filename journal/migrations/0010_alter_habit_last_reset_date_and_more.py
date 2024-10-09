# Generated by Django 5.0.1 on 2024-10-08 15:54

import datetime
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("journal", "0009_userprofile_sissy_name_alter_journalentry_user_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="habit",
            name="last_reset_date",
            field=models.DateField(
                blank=True, default=django.utils.timezone.now, null=True
            ),
        ),
        migrations.AlterField(
            model_name="userfeedback",
            name="timestamp",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 10, 9, 2, 54, 45, 739948)
            ),
        ),
    ]