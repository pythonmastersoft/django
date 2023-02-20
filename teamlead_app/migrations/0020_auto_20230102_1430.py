# Generated by Django 3.0 on 2023-01-02 09:00

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('teamlead_app', '0019_auto_20221228_1633'),
    ]

    operations = [
        migrations.CreateModel(
            name='candidate_application',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('your_name', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('mobile_number', models.DecimalField(decimal_places=0, max_digits=10)),
                ('years_of_experience', models.CharField(blank=True, choices=[('Fresher', 'Fresher'), ('Less than a year', 'Less than a year'), ('1 - 2 years', '1 - 2 years'), ('2 - 4 years', '2 - 4 years'), ('4 - 7 years', '4 - 7 years'), ('7 - 10 years', '7 - 10 years'), ('10+ years', '10+ years')], max_length=30, null=True)),
                ('years_of_relevant_experience', models.CharField(blank=True, choices=[('Fresher', 'Fresher'), ('Less than a year', 'Less than a year'), ('1 - 2 years', '1 - 2 years'), ('2 - 4 years', '2 - 4 years'), ('4 - 7 years', '4 - 7 years'), ('7 - 10 years', '7 - 10 years'), ('10+ years', '10+ years')], max_length=30, null=True)),
                ('resume', models.FileField(upload_to='')),
                ('created_at', models.DateField(default=datetime.datetime(2023, 1, 2, 9, 0, 34, 97076, tzinfo=utc))),
            ],
            options={
                'verbose_name_plural': 'Applied Candidates',
            },
        ),
        migrations.DeleteModel(
            name='Event',
        ),
        migrations.AlterField(
            model_name='applied_for_accounts',
            name='created_at',
            field=models.DateField(default=datetime.datetime(2023, 1, 2, 9, 0, 34, 97076, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='applied_for_development',
            name='created_at',
            field=models.DateField(default=datetime.datetime(2023, 1, 2, 9, 0, 34, 97076, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='applied_for_hr',
            name='created_at',
            field=models.DateField(default=datetime.datetime(2023, 1, 2, 9, 0, 34, 97076, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='applied_for_it',
            name='created_at',
            field=models.DateField(default=datetime.datetime(2023, 1, 2, 9, 0, 34, 97076, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='applied_for_sales',
            name='created_at',
            field=models.DateField(default=datetime.datetime(2023, 1, 2, 9, 0, 34, 97076, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='requirement',
            name='created_at',
            field=models.DateField(default=datetime.datetime(2023, 1, 2, 9, 0, 34, 97076, tzinfo=utc)),
        ),
    ]
