# Generated by Django 3.0 on 2023-02-06 07:31

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('teamlead_app', '0093_auto_20230206_1251'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate_application1',
            name='created_at',
            field=models.DateField(default=datetime.datetime(2023, 2, 6, 7, 31, 48, 664624, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='candidate_master',
            name='created_at',
            field=models.DateField(default=datetime.datetime(2023, 2, 6, 7, 31, 48, 664624, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='recruitment_master',
            name='budget',
            field=models.FloatField(default='0.00', max_length=30),
        ),
        migrations.AlterField(
            model_name='recruitment_master',
            name='created_at',
            field=models.DateField(default=datetime.datetime(2023, 2, 6, 7, 31, 48, 664624, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='scheduled_interview',
            name='time',
            field=models.TimeField(default=datetime.datetime(2023, 2, 6, 7, 31, 48, 664624, tzinfo=utc)),
        ),
    ]
