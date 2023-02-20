import django
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.urls import reverse
import datetime
from datetime import datetime
from django.utils import timezone

#Here we are going to create models(Database tables) for our project.
# Create your models here.

class recruitment_master(models.Model):

    project_choice=(
            ('project name 1', 'project name 1'),
            ('project name 2', 'project name 2'),
            ('project name 3', 'project name 3'),
        )

    # resource_position = (
    #     ('Senior Software Developer', 'Senior Software Developer'),
    #     ('Junior Software Developer', 'Junior Software Developer'),
    #     ('Software Developer Trainee', 'Software Developer Trainee'),
    # )

    resource_type_choice = (
        ('Payroll', 'Payroll'),
        ('Intern', 'Intern'),

    )

    department_choice = (
        ('BUSINESS_DEVELOPMENT', 'BUSINESS DEVELOPMENT'),
        ('DEVELOPMENT', 'DEVELOPMENT'),
        ('HR', 'HR'),
        ('TESTER', 'TESTER'),
        ('IMPLEMENTATION_CCMS', 'IMPLEMENTATION_CCMS'),
        ('CCMS_OTHER', 'CCMS OTHER'),
        ('IMPLEMENTATION_RFC', 'IMPLEMENTATION RFC'),
        ('WEB', 'WEB'),
        ('DIGITAL_MARKETING', 'DIGITAL MARKETING'),
        ('MARKETING', 'PRE-MARKETING'),
        ('ACCOUNTS', 'ACCOUNTS'),
        ('ADMIN', 'ADMIN'),
        ('TECH_IT', 'TECH IT'),
        ('MANAGEMENT', 'MANAGEMENT'),

    )

    posting_location_choice = (
        ('Nagpur', 'Nagpur'),
        ('Pune', 'Pune'),
        ('Mumbai', 'Mumbai'),
        ('Aurangabad', 'Aurangabad'),
    )

    requestor_name = models.CharField(max_length=30)
    project_name = models.CharField(max_length=30, default='Not Inserted')
    department = models.CharField(max_length=30,blank=True, null=True, choices=department_choice)
    position = models.CharField(max_length=30)
    type_of_resource = models.CharField(max_length=30, blank=True, null=True, choices=resource_type_choice)
    posting_location = models.CharField(max_length=30,blank=True, null=True, choices=posting_location_choice)
    experience_required = models.IntegerField()
    technologies_required = models.CharField(max_length=100)
    special_remark = models.CharField(max_length=100)
    no_of_positions = models.IntegerField()
    created_at = models.DateField(default=timezone.now())
    budget = models.FloatField(default=0.00)

    class Meta:
        verbose_name_plural = "Recruitment Master"
    # Method to show name of an object in the database (Django admin pannel and sql database)
    def __str__(self):
        return 'Raised By: ' + self.requestor_name




class document(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    mobile_number = models.CharField(max_length=10)
    Address_Proof = models.FileField()
    pancard = models.FileField()
    Photo_Identity_Proof =  models.FileField()
    HSC_Certificate = models.FileField()
    Diploma_Certificate = models.FileField()
    Degree_Certificate = models.FileField()
    PG_Certificate = models.FileField()
    College_TC = models.FileField()
    Passport_Size_Photograph =  models.FileField()
    Casual_Photograph = models.FileField()
    Bank_Passbook = models.FileField()
    Internship_Certificate = models.FileField()
    Experience_Certificate =  models.FileField()
    Last_3_Salary_Slips =  models.FileField()
    Form_16 = models.FileField()
    Passport = models.FileField()
    Covid_Vaccination_Certificate = models.FileField()
    Medical_Certificate = models.FileField()
    Police_Verification_Document = models.FileField()


class candidate_master(models.Model):
    department_choice = (
        ('BUSINESS_DEVELOPMENT', 'BUSINESS DEVELOPMENT'),
        ('DEVELOPMENT', 'DEVELOPMENT'),
        ('HR', 'HR'),
        ('TESTER', 'TESTER'),
        ('IMPLEMENTATION_CCMS', 'IMPLEMENTATION_CCMS'),
        ('CCMS_OTHER', 'CCMS OTHER'),
        ('IMPLEMENTATION_RFC', 'IMPLEMENTATION RFC'),
        ('WEB', 'WEB'),
        ('DIGITAL_MARKETING', 'DIGITAL MARKETING'),
        ('MARKETING', 'PRE-MARKETING'),
        ('ACCOUNTS', 'ACCOUNTS'),
        ('ADMIN', 'ADMIN'),
        ('TECH_IT', 'TECH IT'),
        ('MANAGEMENT', 'MANAGEMENT'),

    )

    years_of_experience = (
        ('Fresher', 'Fresher'),
        ('Less than a year', 'Less than a year'),
        ('1 - 2 years', '1 - 2 years'),
        ('2 - 4 years', '2 - 4 years'),
        ('4 - 7 years', '4 - 7 years'),
        ('7 - 10 years', '7 - 10 years'),
        ('10+ years', '10+ years'),
    )

    years_of_relevant_experience = (
        ('Fresher', 'Fresher'),
        ('Less than a year', 'Less than a year'),
        ('1 - 2 years', '1 - 2 years'),
        ('2 - 4 years', '2 - 4 years'),
        ('4 - 7 years', '4 - 7 years'),
        ('7 - 10 years', '7 - 10 years'),
        ('10+ years', '10+ years'),
    )

    your_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    mobile_number = models.DecimalField(max_digits=10,decimal_places=0)
    years_of_experience = models.CharField(max_length=30,blank=True, null=True, choices=years_of_experience)
    years_of_relevant_experience = models.CharField(max_length=30,blank=True, null=True, choices=years_of_relevant_experience)
    resume = models.FileField()
    department = models.CharField(max_length=30, blank=True, null=True, choices=department_choice)
    position = models.CharField(max_length=30,default='Not selected ')
    created_at = models.DateField(default=timezone.now())
    current_ctc = models.CharField(max_length=50,default='null')
    expected_ctc = models.CharField(max_length=50,default='null')
    ready_to_relocate = models.CharField(max_length=10)

    class Meta:
        verbose_name_plural = "Candidate Master"

    def __str__(self):
        return self.your_name


class candidate_application(models.Model):
    department_choice = (
        ('BUSINESS_DEVELOPMENT', 'BUSINESS DEVELOPMENT'),
        ('DEVELOPMENT', 'DEVELOPMENT'),
        ('HR', 'HR'),
        ('TESTER', 'TESTER'),
        ('IMPLEMENTATION_CCMS', 'IMPLEMENTATION_CCMS'),
        ('CCMS_OTHER', 'CCMS OTHER'),
        ('IMPLEMENTATION_RFC', 'IMPLEMENTATION RFC'),
        ('WEB', 'WEB'),
        ('DIGITAL_MARKETING', 'DIGITAL MARKETING'),
        ('MARKETING', 'PRE-MARKETING'),
        ('ACCOUNTS', 'ACCOUNTS'),
        ('ADMIN', 'ADMIN'),
        ('TECH_IT', 'TECH IT'),
        ('MANAGEMENT', 'MANAGEMENT'),

    )

    years_of_experience = (
        ('Fresher', 'Fresher'),
        ('Less than a year', 'Less than a year'),
        ('1 - 2 years', '1 - 2 years'),
        ('2 - 4 years', '2 - 4 years'),
        ('4 - 7 years', '4 - 7 years'),
        ('7 - 10 years', '7 - 10 years'),
        ('10+ years', '10+ years'),
    )

    years_of_relevant_experience = (
        ('Fresher', 'Fresher'),
        ('Less than a year', 'Less than a year'),
        ('1 - 2 years', '1 - 2 years'),
        ('2 - 4 years', '2 - 4 years'),
        ('4 - 7 years', '4 - 7 years'),
        ('7 - 10 years', '7 - 10 years'),
        ('10+ years', '10+ years'),
    )

    relocate = (
        ('YES', 'YES'),
        ('NO','NO')
    )


    your_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    mobile_number = models.DecimalField(max_digits=10,decimal_places=0)
    years_of_experience = models.CharField(max_length=30,blank=True, null=True, choices=years_of_experience)
    years_of_relevant_experience = models.CharField(max_length=30,blank=True, null=True, choices=years_of_relevant_experience)
    resume = models.FileField()
    department = models.CharField(max_length=30, blank=True, null=True, choices=department_choice)
    position = models.CharField(max_length=30,default='Not selected ')
    created_at = models.DateField(default=timezone.now())
    current_ctc = models.CharField(max_length=50,default='null')
    expected_ctc = models.CharField(max_length=50,default='null')
    ready_to_relocate = models.CharField(max_length=30, blank=True, null=True, choices=relocate)

    class Meta:
        verbose_name_plural = "Applied Candidates"

    def __str__(self):
        return 'Applicant: ' + self.your_name




# Interviewer Bank table in db
class optional_interviewer_bank(models.Model):

    employee_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    mobile_number = models.DecimalField(max_digits=10, decimal_places=0)

    #To give the name to the database table
    class Meta:
        verbose_name_plural = "Optional Interviewer Bank"

    def __str__(self):
        return self.department+ ': Interviewer: ' + self.employee_name


class scheduled_interview(models.Model):
    mode = (
        ('Online', 'Online'),
        ('Offline', 'Offline'),

    )

    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    contact_no = models.DecimalField(max_digits=10, decimal_places=0)
    department = models.CharField(max_length=100)
    mode = models.CharField(max_length=100,blank=True, null=True, choices=mode)
    round = models.CharField(default='Schedule',max_length=100,blank=True, null=True)
    round_two = models.CharField(default='Schedule',max_length=100, blank=True, null=True)
    machine_test = models.CharField(default='Schedule',max_length=100)
    hr_round = models.CharField(default='Schedule',max_length=100)
    google_meet_link = models.CharField(max_length=500, blank=True, null=True)
    date = models.DateField(blank=True,null=True)
    position = models.CharField(max_length=100)
    time = models.TimeField(default=timezone.now())


    class Meta:
        verbose_name_plural = "Scheduled Interview of Candidates"

    def __str__(self):
        return 'Interview Scheduled: ' + ' For ' + self.department + ' department '



class selected_candidate_interview(models.Model):


    your_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    contact_no = models.DecimalField(max_digits=10, decimal_places=0)
    department = models.CharField(max_length=100)
    position = models.CharField(max_length=30,)
    current_ctc = models.CharField(max_length=50,)
    expected_ctc = models.CharField(max_length=50,)
    resume = models.FileField()

    class Meta:
        verbose_name_plural = "selected candidate for interview"

    def __str__(self):
        return self.your_name + ' selected for interview'


class test_model(models.Model):
    department = (

        ('IT', 'IT'),
        ('HR', 'HR'),
        ('MARKETING', 'MARKETING'),
    )
    department = models.CharField(max_length=100, blank=True, null=True, choices=department)
    position = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "test model"



# Interviewer Bank table in db
class total_interviewer_bank(models.Model):

    employee_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)


    #To give the name to the database table
    class Meta:
        verbose_name_plural = "Total Interviewer Bank"

    def __str__(self):
        return  ': Interviewer: ' + self.employee_name


