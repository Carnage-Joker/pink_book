# Generated by Django 5.1.2 on 2025-02-03 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dressup", "0005_remove_avatar_accessories_remove_avatar_shoes_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="avatar",
            name="story_started",
            field=models.BooleanField(default=False),
        ),
    ]
