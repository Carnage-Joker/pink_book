# Generated by Django 5.1.3 on 2025-01-03 00:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dressup', '0016_alter_purchaseditem_unique_together'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='photoshoot',
            name='backdrop',
        ),
        migrations.RemoveField(
            model_name='photoshoot',
            name='user',
        ),
        migrations.RemoveField(
            model_name='avatar',
            name='hair_color',
        ),
        migrations.RemoveField(
            model_name='purchaseditem',
            name='used',
        ),
        migrations.AlterField(
            model_name='avatar',
            name='body',
            field=models.CharField(choices=[('00', 'Straight'), ('01', 'Petite'), ('02', 'Curvy'), ('03', 'Hourglass')], default='00', max_length=2),
        ),
        migrations.AlterField(
            model_name='avatar',
            name='equipped_items',
            field=models.ManyToManyField(blank=True, related_name='equipped_on_avatars', to='dressup.item'),
        ),
        migrations.AlterField(
            model_name='avatar',
            name='hair',
            field=models.CharField(choices=[('00', 'Short'), ('01', 'Wavy'), ('02', 'Long')], default='00', max_length=20),
        ),
        migrations.AlterField(
            model_name='avatar',
            name='skin',
            field=models.CharField(choices=[('00', 'Light'), ('01', 'Tan'), ('02', 'Dark')], default='00', max_length=2),
        ),
        migrations.DeleteModel(
            name='LeaderboardEntry',
        ),
        migrations.DeleteModel(
            name='PhotoShoot',
        ),
    ]
