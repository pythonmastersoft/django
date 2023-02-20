# Generated by Django 3.0 on 2023-01-02 12:16

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('teamlead_app', '0021_auto_20230102_1503'),
    ]

    operations = [
        migrations.CreateModel(
            name='scheduled_interview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=100)),
                ('contact_no', models.DecimalField(decimal_places=0, max_digits=10)),
                ('department', models.CharField(max_length=30)),
                ('mode', models.CharField(blank=True, choices=[('online', 'online'), ('offline', 'offline')], max_length=30, null=True)),
                ('google_meet_link', models.CharField(blank=True, max_length=200, null=True)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
            ],
        ),
        migrations.AlterField(
            model_name='candidate_application',
            name='created_at',
            field=models.DateField(default=datetime.datetime(2023, 1, 2, 12, 15, 59, 991689, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='requirement',
            name='created_at',
            field=models.DateField(default=datetime.datetime(2023, 1, 2, 12, 15, 59, 991689, tzinfo=utc)),
        ),
    ]
