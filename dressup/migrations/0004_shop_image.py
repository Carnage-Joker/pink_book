# Generated by Django 5.1.3 on 2024-12-08 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dressup', '0003_alter_avatar_hair_alter_avatar_hair_color_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='shops/'),
        ),
    ]