# Generated by Django 3.0 on 2023-02-04 06:28

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('teamlead_app', '0077_auto_20230204_1150'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='master_candidate',
            options={'verbose_name_plural': 'Master Candidate'},
        ),
        migrations.RenameField(
            model_name='master_candidate',
            old_name='ready_to_relocate',
            new_name='relocate',
        ),
        migrations.AlterField(
            model_name='candidate_application1',
            name='created_at',
            field=models.DateField(default=datetime.datetime(2023, 2, 4, 6, 28, 13, 605059, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='master_candidate',
            name='created_at',
            field=models.DateField(default=datetime.datetime(2023, 2, 4, 6, 28, 13, 605059, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='requirement',
            name='created_at',
            field=models.DateField(default=datetime.datetime(2023, 2, 4, 6, 28, 13, 605059, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='scheduled_interview',
            name='time',
            field=models.TimeField(default=datetime.datetime(2023, 2, 4, 6, 28, 13, 605059, tzinfo=utc)),
        ),
    ]
