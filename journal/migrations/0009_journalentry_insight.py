# Generated by Django 4.2.4 on 2023-09-15 04:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("journal", "0008_remove_journalentry_prompt"),
    ]

    operations = [
        migrations.AddField(
            model_name="journalentry",
            name="insight",
            field=models.TextField(blank=True, null=True),
        ),
    ]