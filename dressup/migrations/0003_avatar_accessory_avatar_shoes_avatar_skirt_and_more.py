# Generated by Django 5.1.2 on 2025-04-11 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dressup", "0002_alter_avatar_hair_color_alter_item_category_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="avatar",
            name="accessory",
            field=models.CharField(default="00", max_length=2),
        ),
        migrations.AddField(
            model_name="avatar",
            name="shoes",
            field=models.CharField(default="00", max_length=2),
        ),
        migrations.AddField(
            model_name="avatar",
            name="skirt",
            field=models.CharField(default="00", max_length=2),
        ),
        migrations.AddField(
            model_name="avatar",
            name="top",
            field=models.CharField(default="00", max_length=2),
        ),
    ]
