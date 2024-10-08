# Generated by Django 5.0.1 on 2024-08-08 02:09

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("dressup", "0005_alter_avatar_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="avatar",
            name="accessories",
            field=models.ImageField(upload_to="avatars/accessories/"),
        ),
        migrations.AlterField(
            model_name="avatar",
            name="body",
            field=models.ImageField(upload_to="avatars/body/"),
        ),
        migrations.AlterField(
            model_name="avatar",
            name="bottom",
            field=models.ImageField(upload_to="avatars/bottom/"),
        ),
        migrations.AlterField(
            model_name="avatar",
            name="eyes",
            field=models.ImageField(upload_to="avatars/eyes/"),
        ),
        migrations.AlterField(
            model_name="avatar",
            name="hair",
            field=models.ImageField(upload_to="avatars/hair/"),
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
