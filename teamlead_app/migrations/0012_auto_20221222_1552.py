# Generated by Django 3.0 on 2022-12-22 10:22

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('teamlead_app', '0011_auto_20221222_1432'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requirement',
            name='created_at',
            field=models.DateField(default=datetime.datetime(2022, 12, 22, 10, 22, 43, 222422, tzinfo=utc)),
        ),
    ]
