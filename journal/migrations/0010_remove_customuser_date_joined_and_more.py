# Generated by Django 5.0.1 on 2024-08-04 06:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("journal", "0009_alter_userfeedback_timestamp"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="customuser",
            name="date_joined",
        ),
        migrations.AlterField(
            model_name="customuser",
            name="avatar_body",
            field=models.CharField(
                default="/static/virtual_try_on/avatars/body/light/hourglass.png",
                max_length=255,
            ),
        ),
        migrations.AlterField(
            model_name="customuser",
            name="avatar_bottom",
            field=models.CharField(
                default="/static/virtual_try_on/garmets/skirts/1.png", max_length=255
            ),
        ),
        migrations.AlterField(
            model_name="customuser",
            name="avatar_hair",
            field=models.CharField(
                default="/static/virtual_try_on/avatars/hair/long_straight/blonde.png",
                max_length=255,
            ),
        ),
        migrations.AlterField(
            model_name="customuser",
            name="avatar_shoes",
            field=models.CharField(
                default="/static/virtual_try_on/garmets/shoes/1.png", max_length=255
            ),
        ),
        migrations.AlterField(
            model_name="customuser",
            name="avatar_top",
            field=models.CharField(
                default="/static/virtual_try_on/garmets/tops/1.png", max_length=255
            ),
        ),
        migrations.AlterField(
            model_name="userfeedback",
            name="timestamp",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 8, 4, 16, 50, 12, 544254)
            ),
        ),
    ]