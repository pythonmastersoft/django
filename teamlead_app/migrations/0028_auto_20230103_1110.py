# Generated by Django 3.0 on 2023-01-03 05:40

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('teamlead_app', '0027_auto_20230103_1101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate_application',
            name='created_at',
            field=models.DateField(default=datetime.datetime(2023, 1, 3, 5, 40, 35, 39125, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='requirement',
            name='created_at',
            field=models.DateField(default=datetime.datetime(2023, 1, 3, 5, 40, 35, 39125, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='scheduled_interview',
            name='time',
            field=models.TimeField(default=datetime.datetime(2023, 1, 3, 5, 40, 35, 39125, tzinfo=utc)),
        ),
    ]
