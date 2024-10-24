# Generated by Django 5.0.1 on 2024-10-11 21:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("journal", "0023_rename_user_comment_author_remove_comment_post_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="comment",
            old_name="author",
            new_name="user",
        ),
        migrations.AlterField(
            model_name="userfeedback",
            name="timestamp",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 10, 12, 8, 25, 15, 209739)
            ),
        ),
    ]
