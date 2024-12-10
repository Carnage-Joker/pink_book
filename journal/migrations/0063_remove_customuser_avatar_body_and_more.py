# Generated by Django 5.1.3 on 2024-12-01 12:48

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0062_alter_customuser_is_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='avatar_body',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='avatar_bottom',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='avatar_hair',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='avatar_shoes',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='avatar_top',
        ),
        migrations.CreateModel(
            name='Avatar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('body', models.CharField(default='01', max_length=2)),
                ('hair', models.CharField(default='01', max_length=2)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='avatar', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]