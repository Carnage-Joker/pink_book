# Generated by Django 5.0.1 on 2024-10-04 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dressup", "0009_alter_avatar_user_alter_item_category_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="avatar",
            name="body",
            field=models.ImageField(blank=True, null=True, upload_to="avatars/body/"),
        ),
        migrations.AlterField(
            model_name="avatar",
            name="bottom",
            field=models.ImageField(blank=True, null=True, upload_to="avatars/bottom/"),
        ),
        migrations.AlterField(
            model_name="avatar",
            name="eyes",
            field=models.ImageField(blank=True, null=True, upload_to="avatars/eyes/"),
        ),
        migrations.AlterField(
            model_name="avatar",
            name="hair",
            field=models.ImageField(blank=True, null=True, upload_to="avatars/hair/"),
        ),
        migrations.AlterField(
            model_name="avatar",
            name="shoes",
            field=models.ImageField(blank=True, null=True, upload_to="avatars/shoes/"),
        ),
        migrations.AlterField(
            model_name="avatar",
            name="top",
            field=models.ImageField(blank=True, null=True, upload_to="avatars/top/"),
        ),
    ]
