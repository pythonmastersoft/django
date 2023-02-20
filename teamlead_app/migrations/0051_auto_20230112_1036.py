# Generated by Django 3.0 on 2023-01-12 05:06

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('teamlead_app', '0050_auto_20230112_1034'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate_application',
            name='created_at',
            field=models.DateField(default=datetime.datetime(2023, 1, 12, 5, 6, 28, 460000, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='requirement',
            name='created_at',
            field=models.DateField(default=datetime.datetime(2023, 1, 12, 5, 6, 28, 460000, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='requirement',
            name='department',
            field=models.CharField(choices=[('BUSINESS DEVELOPMENT', 'BUSINESS DEVELOPMENT'), ('development', 'development'), ('HR', 'HR'), ('TESTER', 'TESTER'), ('IMPLEMENTATION CCMS', 'IMPLEMENTATION CCMS'), ('CCMS OTHER', 'CCMS OTHER'), ('IMPLEMENTATION RFC', 'IMPLEMENTATION RFC'), ('WEB', 'WEB'), ('DIGITAL MARKETING', 'DIGITAL MARKETING'), ('MARKETING', 'PRE-MARKETING'), ('ACCOUNTS', 'ACCOUNTS'), ('ADMIN', 'ADMIN'), ('TECH IT', 'TECH IT'), ('MANAGEMENT', 'MANAGEMENT')], max_length=30),
        ),
        migrations.AlterField(
            model_name='scheduled_interview',
            name='time',
            field=models.TimeField(default=datetime.datetime(2023, 1, 12, 5, 6, 28, 460000, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='selected_candidate_interview',
            name='created_at',
            field=models.DateField(default=datetime.datetime(2023, 1, 12, 5, 6, 28, 460000, tzinfo=utc)),
        ),
    ]
