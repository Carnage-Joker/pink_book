# Generated by Django 5.1.2 on 2025-02-02 23:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dressup", "0003_avatar_equipped_items"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="avatar",
            name="created_at",
        ),
        migrations.RemoveField(
            model_name="avatar",
            name="image_path",
        ),
        migrations.RemoveField(
            model_name="avatar",
            name="purchased_items",
        ),
        migrations.AddField(
            model_name="avatar",
            name="story_started",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="avatar",
            name="equipped_items",
            field=models.ManyToManyField(
                blank=True, related_name="equipped_on_avatars", to="dressup.item"
            ),
        ),
        migrations.AlterField(
            model_name="avatar",
            name="hair_color",
            field=models.CharField(
                choices=[
                    ("01", "black"),
                    ("02", "brown"),
                    ("03", "blonde"),
                    ("04", "red"),
                    ("05", "blue"),
                    ("06", "green"),
                    ("07", "purple"),
                    ("08", "pink"),
                    ("09", "rainbow"),
                ],
                default="01",
                max_length=10,
            ),
        ),
        migrations.AlterField(
            model_name="avatar",
            name="skin",
            field=models.CharField(
                choices=[
                    ("01", "light"),
                    ("02", "medium"),
                    ("03", "dark"),
                    ("04", "pale"),
                    ("05", "tan"),
                ],
                default="01",
                max_length=10,
            ),
        ),
    ]
