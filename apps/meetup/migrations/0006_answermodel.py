# Generated by Django 2.2 on 2019-05-01 16:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('meetup', '0005_auto_20190429_1156'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnswerModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.TextField()),
                ('answered_on', models.DateTimeField(auto_now_add=True)),
                ('answered_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('for_question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='meetup.QuestionModel')),
            ],
        ),
    ]
