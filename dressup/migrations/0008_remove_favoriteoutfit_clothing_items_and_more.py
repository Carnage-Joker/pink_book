# Generated by Django 5.0.1 on 2024-10-03 23:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dressup", "0007_clothingitem_photoshootlocation_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="favoriteoutfit",
            name="clothing_items",
        ),
        migrations.RemoveField(
            model_name="favoriteoutfit",
            name="user",
        ),
        migrations.DeleteModel(
            name="PhotoshootLocation",
        ),
        migrations.RenameField(
            model_name="item",
            old_name="is_premium",
            new_name="premium",
        ),
        migrations.RemoveField(
            model_name="avatar",
            name="created_at",
        ),
        migrations.AlterField(
            model_name="avatar",
            name="bottom",
            field=models.ImageField(upload_to="avatars/bottom/"),
        ),
        migrations.AlterField(
            model_name="avatar",
            name="id",
            field=models.AutoField(primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name="avatar",
            name="shoes",
            field=models.ImageField(upload_to="avatars/shoes/"),
        ),
        migrations.AlterField(
            model_name="avatar",
            name="top",
            field=models.ImageField(upload_to="avatars/top/"),
        ),
    ]
