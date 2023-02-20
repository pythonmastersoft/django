# Generated by Django 3.0 on 2023-02-04 09:16

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('teamlead_app', '0085_auto_20230204_1316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate_application1',
            name='created_at',
            field=models.DateField(default=datetime.datetime(2023, 2, 4, 9, 16, 8, 648378, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='candidate_master',
            name='created_at',
            field=models.DateField(default=datetime.datetime(2023, 2, 4, 9, 16, 8, 648378, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='candidate_master',
            name='ready_to_relocate',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='requirement',
            name='created_at',
            field=models.DateField(default=datetime.datetime(2023, 2, 4, 9, 16, 8, 648378, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='scheduled_interview',
            name='time',
            field=models.TimeField(default=datetime.datetime(2023, 2, 4, 9, 16, 8, 648378, tzinfo=utc)),
        ),
    ]
