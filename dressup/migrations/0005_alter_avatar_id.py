# Generated by Django 5.0.1 on 2024-08-07 17:08

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("dressup", "0004_alter_avatar_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="avatar",
            name="id",
            field=models.AutoField(primary_key=True, serialize=False, unique=True),
        ),
    ]
