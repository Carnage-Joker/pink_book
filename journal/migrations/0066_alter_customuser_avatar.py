# Generated by Django 5.1.3 on 2024-12-11 11:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dressup', '0010_alter_shop_shop_id'),
        ('journal', '0065_customuser_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='avatar',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_avatar', to='dressup.avatar'),
        ),
    ]
