# Generated by Django 2.0.1 on 2018-01-13 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0002_auto_20180113_1450'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lobby',
            name='game_id',
            field=models.UUIDField(blank=True, default='c89067', unique=True),
        ),
    ]
