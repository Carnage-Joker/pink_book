# Generated by Django 5.0.1 on 2024-11-18 23:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("journal", "0053_alter_habit_options_remove_habit_date_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="habit",
            old_name="last_reset_date",
            new_name="last_reset",
        ),
        migrations.RemoveField(
            model_name="habit",
            name="reminder_frequency",
        ),
        migrations.AddField(
            model_name="habit",
            name="frequency",
            field=models.CharField(
                choices=[
                    ("daily", "Daily"),
                    ("weekly", "Weekly"),
                    ("monthly", "Monthly"),
                    ("yearly", "Yearly"),
                ],
                default="daily",
                max_length=10,
            ),
        ),
        migrations.AddField(
            model_name="habit",
            name="target_count",
            field=models.PositiveIntegerField(default=8),
        ),
        migrations.AlterField(
            model_name="habit",
            name="category",
            field=models.CharField(
                choices=[
                    ("sissification_tasks", "Sissification Tasks"),
                    ("domme_tasks", "Domme Tasks"),
                    ("punishment_tasks", "Punishment Tasks"),
                    ("work_tasks", "Work/Study Tasks"),
                    ("self_care_tasks", "Self Care Tasks"),
                    ("chore_tasks", "Chore Tasks"),
                    ("personal_tasks", "Personal Tasks"),
                ],
                default="sissification_tasks",
                max_length=50,
            ),
        ),
    ]