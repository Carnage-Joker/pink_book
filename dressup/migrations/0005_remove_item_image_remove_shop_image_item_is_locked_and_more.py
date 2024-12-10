# Generated by Django 5.1.3 on 2024-12-09 00:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dressup', '0004_shop_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='image',
        ),
        migrations.RemoveField(
            model_name='shop',
            name='image',
        ),
        migrations.AddField(
            model_name='item',
            name='is_locked',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='purchaseditem',
            name='is_equipped',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='shop',
            name='image_path',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='shop',
            name='is_locked',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='shop',
            name='shop_level',
            field=models.CharField(choices=[('basic', 'Basic'), ('premium', 'Premium'), ('cute', 'Cute'), ('hawt', 'Hawt'), ('sexy', 'Sexy')], default='basic', max_length=50),
        ),
    ]