# Generated by Django 5.0.1 on 2024-11-18 23:31

import django.utils.timezone
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("journal", "0052_remove_task_id_alter_task_task_id"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="habit",
            options={"ordering": ["-timestamp"]},
        ),
        migrations.RemoveField(
            model_name="habit",
            name="date",
        ),
        migrations.AlterField(
            model_name="habit",
            name="category",
            field=models.CharField(
                choices=[
                    ("fashion_goals", "Fashion Goals"),
                    ("behavioral_goals", "Behavioral Goals"),
                    ("sissification_tasks", "Sissification Tasks"),
                    ("performance_tasks", "Performance Tasks"),
                    ("chastity_goals", "Chastity Goals"),
                    ("self_care", "Self Care"),
                    ("domme_appreciation", "Domme Appreciation"),
                    ("orders", "Orders"),
                ],
                default="sissification_tasks",
                max_length=50,
            ),
        ),
        migrations.AlterField(
            model_name="habit",
            name="id",
            field=models.UUIDField(
                default=uuid.uuid4, editable=False, primary_key=True, serialize=False
            ),
        ),
        migrations.AlterField(
            model_name="habit",
            name="increment_counter",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="habit",
            name="last_reset_date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="habit",
            name="longest_streak_days",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="habit",
            name="start_date",
            field=models.DateField(default=django.utils.timezone.localdate),
        ),
        migrations.AlterField(
            model_name="habit",
            name="timestamp",
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
