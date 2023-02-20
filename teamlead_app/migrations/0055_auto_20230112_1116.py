# Generated by Django 3.0 on 2023-01-12 05:46

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('teamlead_app', '0054_auto_20230112_1049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate_application',
            name='created_at',
            field=models.DateField(default=datetime.datetime(2023, 1, 12, 5, 46, 41, 137628, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='requirement',
            name='created_at',
            field=models.DateField(default=datetime.datetime(2023, 1, 12, 5, 46, 41, 137628, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='requirement',
            name='department',
            field=models.CharField(blank=True, choices=[('business_development', 'BUSINESS DEVELOPMENT'), ('development', 'DEVELOPMENT'), ('hr', 'HR'), ('tester', 'TESTER'), ('implementation_ccms', 'IMPLEMENTATION CCMS'), ('ccms_other', 'CCMS OTHER'), ('implementation_rfc', 'IMPLEMENTATION RFC'), ('web', 'WEB'), ('digital_marketing', 'DIGITAL MARKETING'), ('marketing', 'PRE-MARKETING'), ('account', 'ACCOUNTS'), ('admin', 'ADMIN'), ('tech_it', 'TECH IT'), ('management', 'MANAGEMENT')], max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='scheduled_interview',
            name='time',
            field=models.TimeField(default=datetime.datetime(2023, 1, 12, 5, 46, 41, 137628, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='selected_candidate_interview',
            name='created_at',
            field=models.DateField(default=datetime.datetime(2023, 1, 12, 5, 46, 41, 137628, tzinfo=utc)),
        ),
    ]
