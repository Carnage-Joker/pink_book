# Generated by Django 5.0.1 on 2024-11-08 07:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("journal", "0036_alter_userfeedback_timestamp"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="subscription_tier",
            field=models.CharField(
                choices=[
                    ("free", "Free"),
                    ("basic", "Basic"),
                    ("premium", "Premium"),
                    ("moderator", "Moderator"),
                    ("admin", "Admin"),
                ],
                default="free",
                max_length=50,
            ),
        ),
        migrations.AlterField(
            model_name="habit",
            name="penalty",
            field=models.CharField(
                blank=True,
                choices=[
                    ("ignore", "Ignore"),
                    ("punishment", "Punishment"),
                    ("task", "Task"),
                    ("points_loss", "Lose Points"),
                    ("none", "None"),
                ],
                max_length=50,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="habit",
            name="reward",
            field=models.CharField(
                blank=True,
                choices=[
                    ("praise", "Praise"),
                    ("points", "Points"),
                    ("gift", "Gift"),
                    ("privilege", "Privilege"),
                    ("none", "None"),
                ],
                max_length=50,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="todo",
            name="penalty",
            field=models.CharField(
                blank=True,
                choices=[
                    ("ignore", "Ignore"),
                    ("punishment", "Punishment"),
                    ("task", "Task"),
                    ("points_loss", "Lose Points"),
                    ("none", "None"),
                ],
                max_length=50,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="todo",
            name="reward",
            field=models.CharField(
                blank=True,
                choices=[
                    ("praise", "Praise"),
                    ("points", "Points"),
                    ("gift", "Gift"),
                    ("privilege", "Privilege"),
                    ("none", "None"),
                ],
                max_length=50,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="userfeedback",
            name="timestamp",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 11, 8, 18, 44, 1, 667470)
            ),
        ),
    ]
