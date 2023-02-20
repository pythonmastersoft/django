# Generated by Django 3.0 on 2023-01-13 12:49

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('teamlead_app', '0060_auto_20230113_1430'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate_application',
            name='created_at',
            field=models.DateField(default=datetime.datetime(2023, 1, 13, 12, 49, 4, 809927, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='requirement',
            name='created_at',
            field=models.DateField(default=datetime.datetime(2023, 1, 13, 12, 49, 4, 808884, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='scheduled_interview',
            name='time',
            field=models.TimeField(default=datetime.datetime(2023, 1, 13, 12, 49, 4, 809927, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='selected_candidate_interview',
            name='created_at',
            field=models.DateField(default=datetime.datetime(2023, 1, 13, 12, 49, 4, 810928, tzinfo=utc)),
        ),
    ]
