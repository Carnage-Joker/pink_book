# Generated by Django 5.0.1 on 2024-08-09 15:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("journal", "0036_remove_billing_subscription_type_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="question",
            old_name="user",
            new_name="author",
        ),
        migrations.AddField(
            model_name="answer",
            name="tags",
            field=models.ManyToManyField(blank=True, to="journal.tag"),
        ),
        migrations.AddField(
            model_name="question",
            name="tags",
            field=models.ManyToManyField(blank=True, to="journal.tag"),
        ),
        migrations.AlterField(
            model_name="userfeedback",
            name="timestamp",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 8, 10, 1, 2, 31, 965754)
            ),
        ),
    ]