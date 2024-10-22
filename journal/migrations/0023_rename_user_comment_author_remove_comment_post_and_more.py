# Generated by Django 5.0.1 on 2024-10-11 21:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("journal", "0022_alter_userfeedback_timestamp"),
    ]

    operations = [
        migrations.RenameField(
            model_name="comment",
            old_name="user",
            new_name="author",
        ),
        migrations.RemoveField(
            model_name="comment",
            name="post",
        ),
        migrations.AlterField(
            model_name="userfeedback",
            name="timestamp",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 10, 12, 8, 12, 10, 5905)
            ),
        ),
    ]
