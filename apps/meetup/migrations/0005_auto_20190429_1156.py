# Generated by Django 2.2 on 2019-04-29 11:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meetup', '0004_auto_20190429_1134'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='votesmodel',
            unique_together=set(),
        ),
    ]
