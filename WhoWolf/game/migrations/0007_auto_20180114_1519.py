# Generated by Django 2.0.1 on 2018-01-14 14:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0006_auto_20180113_1619'),
    ]

    operations = [
        migrations.AddField(
            model_name='lobby',
            name='round',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='player',
            name='role',
            field=models.CharField(blank=True, choices=[('Werwolf', 'Werwolf'), ('Bewohner', 'Bewohner'), ('Hexe', 'Hexe')], max_length=32),
        ),
        migrations.AlterField(
            model_name='player',
            name='lobby',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='players', to='game.Lobby'),
        ),
    ]
