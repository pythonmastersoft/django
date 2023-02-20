# Generated by Django 3.0 on 2023-01-11 13:06

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('teamlead_app', '0047_auto_20230111_1833'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate_application',
            name='created_at',
            field=models.DateField(default=datetime.datetime(2023, 1, 11, 13, 6, 52, 994520, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='requirement',
            name='created_at',
            field=models.DateField(default=datetime.datetime(2023, 1, 11, 13, 6, 52, 994520, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='scheduled_interview',
            name='time',
            field=models.TimeField(default=datetime.datetime(2023, 1, 11, 13, 6, 52, 994520, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='selected_candidate_interview',
            name='created_at',
            field=models.DateField(default=datetime.datetime(2023, 1, 11, 13, 6, 52, 994520, tzinfo=utc)),
        ),
    ]
