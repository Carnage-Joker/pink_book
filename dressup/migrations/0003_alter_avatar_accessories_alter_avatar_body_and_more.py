# Generated by Django 5.0.1 on 2024-08-01 05:53

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("dressup", "0002_item_purchaseditem_alter_avatar_top_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="avatar",
            name="accessories",
            field=models.ImageField(upload_to=None),
        ),
        migrations.AlterField(
            model_name="avatar",
            name="body",
            field=models.ImageField(upload_to=None),
        ),
        migrations.AlterField(
            model_name="avatar",
            name="bottom",
            field=models.ImageField(upload_to=None),
        ),
        migrations.AlterField(
            model_name="avatar",
            name="eyes",
            field=models.ImageField(upload_to=None),
        ),
        migrations.AlterField(
            model_name="avatar",
            name="hair",
            field=models.ImageField(upload_to=None),
        ),
        migrations.AlterField(
            model_name="avatar",
            name="shoes",
            field=models.ImageField(upload_to=None),
        ),
        migrations.AlterField(
            model_name="avatar",
            name="top",
            field=models.ImageField(upload_to=None),
        ),
    ]
