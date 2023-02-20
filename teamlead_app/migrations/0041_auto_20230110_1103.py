# Generated by Django 3.0 on 2023-01-10 05:33

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('teamlead_app', '0040_auto_20230105_1829'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate_application',
            name='created_at',
            field=models.DateField(default=datetime.datetime(2023, 1, 10, 5, 33, 37, 113920, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='requirement',
            name='created_at',
            field=models.DateField(default=datetime.datetime(2023, 1, 10, 5, 33, 37, 113920, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='requirement',
            name='department',
            field=models.CharField(blank=True, choices=[('ANDROID', 'ANDROID'), ('CCMS DEVELOPMENT', 'CCMS DEVELOPMENT'), ('HR', 'HR'), ('CCMS SUPPORT', 'CCMS SUPPORT'), ('FINANCE AND ADMINISTRATION', 'FINANCE AND ADMINISTRATION'), ('HARDWARE AND NETWORKING', 'HARDWARE AND NETWORKING'), ('Library Development', 'Library Development'), ('NON ACADEMIC RFC DEV', 'Non Academic RFC DEV'), ('OBE DEVELOPMENT', 'OBE DEVELOPMENT'), ('PRE-SALES', 'PRE-SALES'), ('PYTHON DEVELOPMENT', 'PYTHON DEVELOPMENT'), ('RFC DEVELOPMENT', 'RFC DEVELOPMENT'), ('RFC SUPPORT', ' RFC SUPPORT'), ('SALES CCMS', 'SALES CCMS'), ('SOFTWARE TESTING', 'SOFTWARE TESTING'), ('WEB DEVELOPMENT', 'WEB DEVELOPMENT'), ('UI DEVELOPMENT', 'UI DEVELOPMENT')], max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='scheduled_interview',
            name='time',
            field=models.TimeField(default=datetime.datetime(2023, 1, 10, 5, 33, 37, 113920, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='selected_candidate_interview',
            name='created_at',
            field=models.DateField(default=datetime.datetime(2023, 1, 10, 5, 33, 37, 113920, tzinfo=utc)),
        ),
    ]
