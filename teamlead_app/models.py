
from django.db import models

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

    requestor_name = models.CharField(max_length=255)
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


class requirement_raised(models.Model):

    project_choice=(
            ('project name 1', 'project name 1'),
            ('project name 2', 'project name 2'),
            ('project name 3', 'project name 3'),
        )
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

    requestor_name = models.CharField(max_length=255)
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
        verbose_name_plural = "requirement Raised Table"
    # Method to show name of an object in the database (Django admin pannel and sql database)

    def __str__(self):
        return 'Raised By: ' + self.requestor_name

    def save(self, *args, **kwargs):
        # Capitalize the first letter of each word in the requestor name before saving
        self.requestor_name = ' '.join(word.capitalize() for word in self.requestor_name.split())
        super().save(*args, **kwargs)




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
    father_name = models.CharField(max_length=100,blank=True, null=True)
    permanent_address = models.CharField(max_length=100,blank=True, null=True)
    mobile_number = models.DecimalField(max_digits=10,decimal_places=0,blank=True, null=True)
    years_of_experience = models.CharField(max_length=30,blank=True, null=True, choices=years_of_experience)
    years_of_relevant_experience = models.CharField(max_length=30,blank=True, null=True, choices=years_of_relevant_experience)
    resume = models.FileField()
    department = models.CharField(max_length=30, blank=True, null=True, choices=department_choice)
    position = models.CharField(max_length=30,default='Not selected',blank=True, null=True)
    created_at = models.DateField(default=timezone.now())
    current_ctc = models.CharField(max_length=50,default='null',blank=True, null=True)
    expected_ctc = models.CharField(max_length=50,default='null',blank=True, null=True)
    ready_to_relocate = models.CharField(max_length=10,blank=True, null=True)
    status = models.CharField(default="NA",max_length=100,blank=True, null=True,)
    address_proof = models.FileField()
    pancard = models.FileField()
    photo_identity_proof = models.FileField()
    ssc_certificate = models.FileField()
    hsc_certificate = models.FileField()
    diploma_certificate = models.FileField()
    degree_certificate = models.FileField()
    pg_certificate = models.FileField()
    college_tc = models.FileField()
    passport_size_photo = models.FileField()
    bank_passbook = models.FileField()
    internship_certificate = models.FileField()
    experience_certificate = models.FileField()
    salary_slip = models.FileField()
    form_16 = models.FileField()
    passport = models.FileField()
    covid_vaccination_certificate = models.FileField()
    medical_certificate = models.FileField()
    police_verification_document = models.FileField()

#
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
    father_name = models.CharField(max_length=100,blank=True, null=True)
    permanent_address = models.CharField(max_length=100,blank=True, null=True)
    mobile_number = models.DecimalField(max_digits=10,decimal_places=0)
    years_of_experience = models.CharField(max_length=30,blank=True, null=True, choices=years_of_experience)
    years_of_relevant_experience = models.CharField(max_length=30,blank=True, null=True, choices=years_of_relevant_experience)
    resume = models.FileField()
    department = models.CharField(max_length=30, blank=True, null=True, choices=department_choice)
    position = models.CharField(max_length=30,default='Not selected ', blank=True, null=True,)
    created_at = models.DateField(default=timezone.now())
    current_ctc = models.CharField(max_length=50,default='null', blank=True, null=True,)
    expected_ctc = models.CharField(max_length=50,default='null', blank=True, null=True,)
    ready_to_relocate = models.CharField(max_length=30, blank=True, null=True, choices=relocate)
    status = models.CharField(default='NA',max_length=30 , blank=True, null=True,)

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
    father_name = models.CharField(max_length=100,blank=True, null=True)
    permanent_address = models.CharField(max_length=100,blank=True, null=True)
    contact_no = models.DecimalField(max_digits=10, decimal_places=0)
    department = models.CharField(max_length=100)
    mode = models.CharField(max_length=100,blank=True, null=True, choices=mode)
    google_meet_link = models.CharField(max_length=500, blank=True, null=True)
    date = models.DateField(blank=True,null=True)
    position = models.CharField(max_length=100)
    time = models.TimeField(default=timezone.now())
    status = models.CharField(default="NA", max_length=100, blank=True, null=True)
    interview_round = models.CharField(default="NA",max_length=200)
    interviewer = models.CharField(max_length=100, blank=True, null=True)
    interviewer_mail = models.CharField(max_length=100, blank=True, null=True)
    feedback_interview1 = models.CharField(default='Not Available',max_length=300)
    feedback_interview2 = models.CharField(default='Not Available',max_length=300)
    feedback_interview3 = models.CharField(default='Not Available',max_length=300)
    additional_round = models.CharField(default='Not Available',max_length=300)
    machine_test = models.CharField(default='Not Available',max_length=300)
    HR_round = models.CharField(default='Not Available',max_length=300)


    class Meta:
        verbose_name_plural = "Scheduled Interview of Candidates"

    def __str__(self):
        return  self.name




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


class upload_document(models.Model):

    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    mobile_number = models.DecimalField(max_digits=10, decimal_places=0)
    address_proof = models.FileField()
    pancard = models.FileField()
    photo_identity_proof = models.FileField()
    ssc_certificate = models.FileField()
    hsc_certificate = models.FileField()
    diploma_certificate = models.FileField()
    degree_certificate = models.FileField()
    pg_certificate = models.FileField()
    college_tc = models.FileField()
    passport_size_photo = models.FileField()
    bank_passbook = models.FileField()
    internship_certificate = models.FileField()
    experience_certificate = models.FileField()
    salary_slip = models.FileField()
    form_16 = models.FileField()
    passport = models.FileField()
    covid_vaccination_certificate = models.FileField()
    medical_certificate = models.FileField()
    police_verification_document = models.FileField()

    # To give the name to the database table
    class Meta:
        verbose_name_plural = "Documents Uploaded by Candidate"

    def __str__(self):
        return ': Interviewer: ' + self.name

class offer_letter_detail(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    father_name = models.CharField(max_length=100,blank=True,null=True)
    permanent_address = models.CharField(max_length=100,blank=True,null=True)
    designation = models.CharField(max_length=100)
    joining_date = models.CharField(max_length=100)
    package = models.CharField(max_length=100,blank=True,null=True)
    package_in_words = models.CharField(max_length=100,blank=True,null=True)
    location = models.CharField(max_length=100)
    emp_code = models.CharField(max_length=100)
    basic_da = models.IntegerField(max_length=100)
    flexible_allowance= models.IntegerField(max_length=100)
    pt = models.IntegerField(max_length=100)
    esic = models.IntegerField(max_length=100)
    comp_esic_contribution = models.IntegerField(max_length=100)
    service_level_agreement = models.CharField(max_length=100,blank=True,null=True)

    # To give the name to the database table
    class Meta:
        verbose_name_plural = "Offer letter details"

    def __str__(self):
        return self.name