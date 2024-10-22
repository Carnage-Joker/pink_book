# Generated by Django 5.0.1 on 2024-10-11 18:37

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("journal", "0020_alter_userfeedback_timestamp"),
    ]

    operations = [
        migrations.AddField(
            model_name="comment",
            name="post",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="comments",
                to="journal.blogpost",
            ),
        ),
        migrations.AlterField(
            model_name="userfeedback",
            name="timestamp",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 10, 12, 5, 37, 47, 723938)
            ),
        ),
    ]
