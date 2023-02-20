# Generated by Django 3.0 on 2023-02-06 06:05

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('teamlead_app', '0090_auto_20230206_1129'),
    ]

    operations = [
        migrations.AddField(
            model_name='requirement_master',
            name='project_name',
            field=models.CharField(default='Not Inserted', max_length=30),
        ),
        migrations.AlterField(
            model_name='candidate_application1',
            name='created_at',
            field=models.DateField(default=datetime.datetime(2023, 2, 6, 6, 5, 20, 583713, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='candidate_master',
            name='created_at',
            field=models.DateField(default=datetime.datetime(2023, 2, 6, 6, 5, 20, 583713, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='requirement_master',
            name='created_at',
            field=models.DateField(default=datetime.datetime(2023, 2, 6, 6, 5, 20, 583713, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='scheduled_interview',
            name='time',
            field=models.TimeField(default=datetime.datetime(2023, 2, 6, 6, 5, 20, 583713, tzinfo=utc)),
        ),
    ]
