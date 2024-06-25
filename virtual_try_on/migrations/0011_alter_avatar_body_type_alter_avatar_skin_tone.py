# Generated by Django 5.0.1 on 2024-06-25 05:21

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("virtual_try_on", "0010_alter_premiumoutfit_price"),
    ]

    operations = [
        migrations.AlterField(
            model_name="avatar",
            name="body_type",
            field=models.CharField(
                choices=[
                    ("hourglass", "Hourglass"),
                    ("thick", "Thick"),
                    ("slim", "Slim"),
                    ("straight", "Straight"),
                ],
                default="hourglass",
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="avatar",
            name="skin_tone",
            field=models.CharField(
                choices=[("light", "Light"), ("brown", "Brown"), ("dark", "Dark")],
                default="light",
                max_length=20,
            ),
        ),
    ]
