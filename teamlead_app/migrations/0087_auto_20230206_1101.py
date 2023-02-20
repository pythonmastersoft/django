# Generated by Django 3.0 on 2023-02-06 05:31

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('teamlead_app', '0086_auto_20230204_1446'),
    ]

    operations = [
        migrations.CreateModel(
            name='requirement_master',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('requestor_name', models.CharField(max_length=30)),
                ('project_name', models.CharField(blank=True, choices=[('project name 1', 'project name 1'), ('project name 2', 'project name 2'), ('project name 3', 'project name 3')], max_length=40, null=True)),
                ('department', models.CharField(blank=True, choices=[('BUSINESS_DEVELOPMENT', 'BUSINESS DEVELOPMENT'), ('DEVELOPMENT', 'DEVELOPMENT'), ('HR', 'HR'), ('TESTER', 'TESTER'), ('IMPLEMENTATION_CCMS', 'IMPLEMENTATION_CCMS'), ('CCMS_OTHER', 'CCMS OTHER'), ('IMPLEMENTATION_RFC', 'IMPLEMENTATION RFC'), ('WEB', 'WEB'), ('DIGITAL_MARKETING', 'DIGITAL MARKETING'), ('MARKETING', 'PRE-MARKETING'), ('ACCOUNTS', 'ACCOUNTS'), ('ADMIN', 'ADMIN'), ('TECH_IT', 'TECH IT'), ('MANAGEMENT', 'MANAGEMENT')], max_length=30, null=True)),
                ('position', models.CharField(max_length=30)),
                ('type_of_resource', models.CharField(blank=True, choices=[('Payroll', 'Payroll'), ('Intern', 'Intern')], max_length=30, null=True)),
                ('posting_location', models.CharField(blank=True, choices=[('Nagpur', 'Nagpur'), ('Pune', 'Pune'), ('Mumbai', 'Mumbai'), ('Aurangabad', 'Aurangabad')], max_length=30, null=True)),
                ('experience_required', models.IntegerField()),
                ('technologies_required', models.CharField(max_length=100)),
                ('special_remark', models.CharField(max_length=100)),
                ('no_of_positions', models.IntegerField()),
                ('created_at', models.DateField(default=datetime.datetime(2023, 2, 6, 5, 31, 17, 175922, tzinfo=utc))),
                ('budget', models.CharField(default=0, max_length=30)),
            ],
        ),
        migrations.DeleteModel(
            name='requirement',
        ),
        migrations.AlterField(
            model_name='candidate_application1',
            name='created_at',
            field=models.DateField(default=datetime.datetime(2023, 2, 6, 5, 31, 17, 175922, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='candidate_master',
            name='created_at',
            field=models.DateField(default=datetime.datetime(2023, 2, 6, 5, 31, 17, 175922, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='scheduled_interview',
            name='time',
            field=models.TimeField(default=datetime.datetime(2023, 2, 6, 5, 31, 17, 175922, tzinfo=utc)),
        ),
    ]
