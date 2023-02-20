# Generated by Django 3.0 on 2023-01-11 12:21

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('teamlead_app', '0044_auto_20230111_1525'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate_application',
            name='created_at',
            field=models.DateField(default=datetime.datetime(2023, 1, 11, 12, 21, 9, 210773, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='requirement',
            name='created_at',
            field=models.DateField(default=datetime.datetime(2023, 1, 11, 12, 21, 9, 210773, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='scheduled_interview',
            name='time',
            field=models.TimeField(default=datetime.datetime(2023, 1, 11, 12, 21, 9, 210773, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='selected_candidate_interview',
            name='created_at',
            field=models.DateField(default=datetime.datetime(2023, 1, 11, 12, 21, 9, 226401, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='test_model',
            name='department',
            field=models.CharField(blank=True, choices=[('IT', 'IT'), ('HR', 'HR'), ('MARKETING', 'MARKETING')], max_length=100, null=True),
        ),
    ]
