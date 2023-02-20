# Generated by Django 3.0 on 2023-01-05 11:46

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('teamlead_app', '0035_auto_20230104_1742'),
    ]

    operations = [
        migrations.AddField(
            model_name='selected_candidate_interview',
            name='interviewer_bank',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='teamlead_app.optional_interviewer_bank'),
        ),
        migrations.AlterField(
            model_name='candidate_application',
            name='created_at',
            field=models.DateField(default=datetime.datetime(2023, 1, 5, 11, 46, 11, 380243, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='requirement',
            name='created_at',
            field=models.DateField(default=datetime.datetime(2023, 1, 5, 11, 46, 11, 380243, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='scheduled_interview',
            name='time',
            field=models.TimeField(default=datetime.datetime(2023, 1, 5, 11, 46, 11, 380243, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='selected_candidate_interview',
            name='created_at',
            field=models.DateField(default=datetime.datetime(2023, 1, 5, 11, 46, 11, 380243, tzinfo=utc)),
        ),
    ]
