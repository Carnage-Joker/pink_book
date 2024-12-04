# Generated by Django 5.0.1 on 2024-11-21 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0058_alter_resource_title'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contact',
            options={'ordering': ['-timestamp']},
        ),
        migrations.AlterModelOptions(
            name='resourcecomment',
            options={'ordering': ['-timestamp']},
        ),
        migrations.RemoveField(
            model_name='resource',
            name='category',
        ),
        migrations.AddField(
            model_name='contact',
            name='subject',
            field=models.CharField(default='The Pink Book Rocks!!', max_length=200),
        ),
        migrations.AddField(
            model_name='resource',
            name='featured',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='contact',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='contact',
            name='message',
            field=models.TextField(default='The Pink Book Rocks!!', max_length=750),
        ),
        migrations.AlterField(
            model_name='contact',
            name='name',
            field=models.CharField(max_length=150),
        ),
    ]
