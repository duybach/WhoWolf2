# Generated by Django 2.0.1 on 2018-01-13 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0004_auto_20180113_1505'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lobby',
            name='game_id',
            field=models.CharField(blank=True, max_length=6),
        ),
    ]
