# Generated by Django 5.1.3 on 2024-11-24 21:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0060_alter_contact_email_alter_contact_message_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='is_subscriber',
        ),
    ]
