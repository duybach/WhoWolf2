# Generated by Django 2.0.1 on 2018-01-21 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0017_auto_20180121_1511'),
    ]

    operations = [
        migrations.AddField(
            model_name='lobby',
            name='time_per_round',
            field=models.IntegerField(default=60),
        ),
    ]