import dataclasses

import datetime as datetime

from bs4 import BeautifulSoup
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.mail import send_mail, send_mass_mail
from datetime import datetime, date

from django.views import generic
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.models import User, Group
from datetime import datetime, timedelta, date
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from django.utils.safestring import mark_safe
import calendar
# from .models import requirement
from .models import *
from .templatetags.has_group import register
from google.oauth2 import service_account
from django.conf.urls import include, url
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.views.generic import FormView
from googleapiclient.discovery import build
from django.contrib.messages import error


# Create your views here.


# --------------- Creating decorators to check if the user belongs to the certain group or not -------------------

def is_teamlead(user):
    return user.groups.filter(name='Team_Leads').exists()


def is_Human_Resource(user):
    return user.groups.filter(name='Human_Resource').exists()


def is_Administrator(user):
    return user.groups.filter(name='Administrator').exists()


# ----------------------------------------------------------------------------------------------------------------

# @user_passes_test(is_teamlead)
@login_required
@csrf_exempt
def home(request):
    # group = Group(name="Team_Leads")
    # print("------------------",group)

    user = request.user  # get current User.
    print('---------------------', user)

    if user.groups.filter(name='Team_Leads').exists():
        print("Inside Team lead")
        return redirect(raise_requirement_form)  # Redirecting the control to the raise_requirement_form function


    #  return render(request, "teamlead.html")

    elif user.groups.filter(name='Human_Resource').exists():
        print("inside HR")
        return redirect(hr_view)

        # return redirect('/main_page/calendar')
        # return redirect(CalendarView.as_view)
        # return render(request, "cal/calendar.html")
        # return render(request,'hr.html')


    elif user.groups.filter(name='Administrator').exists():
        print("Inside admin ")
        return render(request, "admin.html")

    elif request.user.is_superuser:
        print(request.user)
        return redirect('/admin')


# #Teamlead Feature 1 a form to raise the requirement to hire a candidate
# @csrf_exempt
# @login_required
# def raise_requirement_form(request):
#     print("Inside raise requirment form ")
#     if request.method == 'POST':
#         requestor_name = request.POST['requestor_name']
#         department = request.POST['department']
#         no_of_positions = request.POST['no_of_positions']
#         position = request.POST['position']
#         type_of_resource = request.POST['type_of_resource']
#         posting_location = request.POST['posting_location']
#         experience_required = request.POST['experience_required']
#         special_remark = request.POST['special_remark']
#         technologies_required = request.POST['technologies_required']
#         project_name = request.POST['project_name']
#
#         data = recruitment_master(department=department, project_name=project_name,
#                                   position=position, type_of_resource=type_of_resource,
#                                   posting_location=posting_location, experience_required=experience_required,
#                                   special_remark=special_remark, technologies_required=technologies_required,
#                                   requestor_name=requestor_name, no_of_positions=no_of_positions)
#         data.save()
#
#         print('Sending the mail notification to HR and Admin')
#
#         # Code for sending the same mail to multiple peoples
#         send_mail(
#            'Requiremnt Raised ',
#            'tesing the mail function.',
#            'prathameshbhuskade.pr17@gmail.com', # Sender of the mail
#            ['prathameshbhuskade.pr17@gmail.com','prathameshbhuskade@gmail.com'], # HR Mail id and admin mail id (Reciever)
#            fail_silently=False
#         )
#
#         # For sending the diffrent mails to the diffrent mail id
#         datatuple = (
#             ('Subject', 'Message.', 'from@example.com', ['john@example.com']),
#             ('Subject', 'Message.', 'from@example.com', ['jane@example.com']),
#         )
#         send_mass_mail(datatuple)
#
#         print('Mail Send sucess')
#
#     return render(request, 'teamlead/home.html')


# Creating the calender for scheduling the interviews in Hr View

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import UserRegistrationForm
from django.contrib.auth.models import Group


def index(request):
    return redirect('login')

@login_required
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():

            user_group = form.cleaned_data['user_group']
            print('============================================================================')
            print(user_group)
            print('============================================================================')
            user = form.save(
                commit=False)  # get the model instance from the filled-out form without saving it to the database

            if user_group == 'Teamlead':
                user.is_staff = True
                user.save()  # Saving the user in the database
                group1 = Group.objects.get(name='Team_Leads')
                user.groups.add(group1)
            else:
                user = form.save(commit=False)
                user.is_staff = True  # setting the staff status to access the admin pannel with given permissions
                user.save()  # Saving the user in the database
                group2 = Group.objects.get(name='Human_Resource')
                user.groups.add(group2)
                # form.save_m2m()   for handling any many-to-many relationships that are not saved when commit=False
            messages.success(request, f'Your account has been created. You can log in now!')
            return redirect('/')
    else:
        form = UserRegistrationForm()

    context = {'form': form}
    return render(request, 'register.html', context)


# --------------------HR views starts from here---------------------------------------------------------------

# Raise requirement feature for HR view

@login_required
def hr_view(request):
    user = request.user
    print("Inside HR view", user)
    if request.user.is_authenticated and user.groups.filter(name='Human_Resource').exists():
        if recruitment_master.objects.all().values():
            all_objects = recruitment_master.objects.all().values()
            context = {'all_objects': all_objects}
            return render(request, 'HR/current_requirement.html', context)

        return render(request, 'HR/current_requirement.html')

    else:
        print("You don't have access to HR View", request.user)
        return redirect('/login')


@csrf_exempt
@login_required
def hr_raise_requirement(request):
    user = request.user
    # request.session['user'] = user.id
    # user_session = request.session['user']
    # print('user session is==',user_session)

    print("Inside HR view", user)
    if request.user.is_authenticated and user.groups.filter(name='Human_Resource').exists():
        print("authenticated user", user)

        if request.method == 'POST':
            requestor_name = request.POST['requestor_name']
            department = request.POST['department']
            no_of_positions = request.POST['no_of_positions']
            position = request.POST['position']
            type_of_resource = request.POST['type_of_resource']
            posting_location = request.POST['posting_location']
            experience_required = request.POST['experience_required']
            special_remark = request.POST['special_remark']
            technologies_required = request.POST['technologies_required']
            project_name = request.POST['project_name']
            print(position)
            print(department)

            data = recruitment_master( department=department,project_name=project_name,
                               position=position, type_of_resource=type_of_resource,
                               posting_location=posting_location, experience_required=experience_required,
                               special_remark=special_remark, technologies_required=technologies_required,
                               requestor_name=requestor_name, no_of_positions=no_of_positions)
            data.save()
            print("Sending Mail....")

            # Code for sending the mail
            # send_mail(
            #     'Requiremnt Raised ',
            #     'tesing the mail function.',
            #     'prathameshbhuskade.pr17@gmail.com',#Sender of the mail
            #     ['prathameshbhuskade.pr17@gmail.com', 'prathameshbhuskade@gmail.com'],
            #     # HR Mail id and admin mail id (Reciever)
            #     fail_silently=False
            # )

            return render(request, 'HR/home.html')

        return render(request, 'HR/home.html')

    else:
        print("You don't have access to HR View", request.user)
        return redirect('/login')

@login_required
def update_budget(request):
    return render('HR/current_requiremnet')


# def hr_view(request):
#     if request.user.is_authenticated:
#         form = recruitment_by_hr_form(request.POST)
#         context = {'form': form}
#         return render(request, 'HR/home.html', context)
#     else:
#         print("You are not logeed in" ,request.user)
#         return redirect('/login')


@csrf_exempt
@login_required
def raise_requirement_form(request):
    if request.method == 'POST':
        requestor_name = request.POST.get('requestor_name')
        department = request.POST['department']
        no_of_positions = request.POST['no_of_positions']
        position = request.POST['position']
        type_of_resource = request.POST['type_of_resource']
        posting_location = request.POST['posting_location']
        experience_required = request.POST['experience_required']
        special_remark = request.POST['special_remark']
        technologies_required = request.POST['technologies_required']
        project_name = request.POST['project_name']

        data = recruitment_master(department=department, project_name=project_name,
                                  position=position, type_of_resource=type_of_resource,
                                  posting_location=posting_location, experience_required=experience_required,
                                  special_remark=special_remark, technologies_required=technologies_required,
                                  requestor_name=requestor_name, no_of_positions=no_of_positions)
        data.save()

        print("Sending Mail....")

        # Code for sending the mail
        send_mail(
            'Requiremnt Raised ',
            'tesing the mail function.',
            'prathameshbhuskade.pr17@gmail.com',  # Sender of the mail
            ['prathameshbhuskade.pr17@gmail.com', 'prathameshbhuskade@gmail.com'],
            # HR Mail id and admin mail id (Reciever)
            fail_silently=False
        )

        # For sending the diffrent mails to the diffrent mail id
        # datatuple = (
        #         ('Subject', 'Message.', 'from@example.com', ['john@example.com']),
        #         ('Subject', 'Message.', 'from@example.com', ['jane@example.com']),
        #     )
        # send_mass_mail(datatuple)
        #
        print('Mail Send sucess')

        return render(request, 'teamlead/home.html')

    return render(request, 'teamlead/home.html')


# Teamlead 2nd feature
def current_requirement(request):
    if recruitment_master.objects.all().values():
        all_objects = recruitment_master.objects.all().values()
        context = {'all_objects': all_objects}
        return render(request, 'current_requirement.html', context)

    return render(request, 'current_requirement.html')




# Candidate Applciation Form
def Apply_form(request):
    if request.method == 'POST':
        your_name = request.POST['your_name']
        email = request.POST['email']
        mobile_number = request.POST['mobile_number']
        years_of_experience = request.POST['years_of_experience']
        years_of_relevant_experience = request.POST['years_of_relevant_experience']
        current_ctc = request.POST['current_ctc']
        expected_ctc = request.POST['expected_ctc']
        resume = request.FILES['resume']
        department = request.POST['department']
        ready_to_relocate = request.POST.get('ready_to_relocate')
        position = request.POST['position']
        data = candidate_master(your_name=your_name, email=email, mobile_number=mobile_number,
                                     years_of_experience=years_of_experience, current_ctc=current_ctc,
                                     expected_ctc=expected_ctc,
                                     years_of_relevant_experience=years_of_relevant_experience,department=department,
                                     position=position, resume=resume,ready_to_relocate=ready_to_relocate,)
        data.save()

        data = candidate_application(your_name=your_name, email=email, mobile_number=mobile_number,
                                years_of_experience=years_of_experience, current_ctc=current_ctc,
                                expected_ctc=expected_ctc,
                                years_of_relevant_experience=years_of_relevant_experience, department=department,
                                position=position, resume=resume, ready_to_relocate=ready_to_relocate,)
        data.save()

        return render(request, 'HR/Apply Pages/apply.html')

    return render(request, 'HR/Apply Pages/apply.html')



# Document Upload Form For Selected Candidate
def document_upload_form(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        mobile_number = request.POST['mobile_number']
        pancard = request.FILES['pancard']
        Address_Proof = request.FILES['address_proof']
        Photo_Identity_Proof = request.FILES['Photo_Identity_Proof']
        SSC_Certificate = request.FILES['SSC_Certificate']
        HSC_Certificate = request.FILES['HSC_Certificate']
        Diploma_Certificate = request.FILES['Diploma_Certificate']
        Degree_Certificate = request.FILES['Degree_Certificate']
        PG_Certificate = request.FILES['PG_Certificate']
        College_TC = request.FILES['College_TC']
        Passport_Size_Photograph = request.FILES['Passport_Size_Photograph']
        Casual_Photograph = request.FILES['Casual_Photograph']
        Bank_Passbook = request.FILES['Bank_Passbook']
        Internship_Certificate = request.FILES['Internship_Certificate']
        Experience_Certificate = request.FILES['Experience_Certificate']
        Last_3_Salary_Slips = request.FILES['Last_3_Salary_Slips']
        Form_16 = request.FILES['Form_16']
        Passport = request.FILES['Passport']
        Covid_Vaccination_Certificate = request.FILES['Covid_Vaccination_Certificate']
        Medical_Certificate = request.FILES['Medical_Certificate']
        Police_Verification_Document = request.FILES['Police_Verification_Document']
        data = document(Address_Proof=Address_Proof, Photo_Identity_Proof=Photo_Identity_Proof,
                        SSC_Certificate=SSC_Certificate,
                        HSC_Certificate=HSC_Certificate,
                        Diploma_Certificate=Diploma_Certificate, Degree_Certificate=Degree_Certificate,
                        PG_Certificate=PG_Certificate, College_TC=College_TC,
                        Passport_Size_Photograph=Passport_Size_Photograph,
                        Casual_Photograph=Casual_Photograph, Bank_Passbook=Bank_Passbook,
                        Internship_Certificate=Internship_Certificate,
                        Experience_Certificate=Experience_Certificate, Last_3_Salary_Slips=Last_3_Salary_Slips,
                        Form_16=Form_16,
                        Passport=Passport, Covid_Vaccination_Certificate=Covid_Vaccination_Certificate,
                        Medical_Certificate=Medical_Certificate,
                        Police_Verification_Document=Police_Verification_Document
                        )

        data.save()
        return render(request, 'Document_upload_from.html')

    return render(request, 'Document_upload_from.html')


from teamlead_app.models import candidate_master


@login_required
def show_applicants(request, id=None):
    get_id = id

    if get_id == None:
        all_objects = candidate_application.objects.all().values()
        context = {'all_objects': all_objects}

        return render(request, 'HR/applicant_data.html', context)

    else:
        return redirect('selected_applicants2', id=get_id)  # this will go to selected_candidate view(function)

    #   object = Candidate_Application.objects.filter(id=get_id).values()
    #   result = list(object)
    #   if result not in lst:    #Preventing the duplicates into the list
    #       lst.append(result)
    #
    #
    # #  print('list=',lst)
    #   for i in lst:
    #       for j in i:
    #           print(j)
    #           if j not in lst2:  # Preventing the duplicates into the list
    #               lst2.append(j)
    #
    #   #print('final',lst2)
    #
    #   context = {'lst2': lst2}
    #
    #
    #   return render(request, 'HR/selected_candidate.html',context)
    #
    # print("Inside else part ")
    # all_objects = Candidate_Application.objects.all().values()
    # context = {'all_objects': all_objects}
    # obj = Candidate_Application.objects.get(id=get_id)
    # context1 = {'obj': obj}
    # return render(request,'HR/applicant_data.html',context,context1)



from django.shortcuts import render, get_object_or_404, redirect
from .forms import UpdateForm


def update_view(request, pk):
    # Retrieve the object to be updated
    obj = get_object_or_404(recruitment_master, pk=pk)

    # Create the form instanc e with the retrieved object
    form = UpdateForm(request.POST or None, instance=obj)

    # Check if the form is being submitted
    if request.method == 'POST':
        # Validate the form
        if form.is_valid():
            # Save the updated object
            form.save()
            # Redirect to the success page
            return redirect('success')

    # Render the template
    return render(request, 'update.html', {'form': form})


# Selected candidate For interview process
@login_required
def selected_candidate(request, id):
    print("Inside selected candidate function")
    get_id = id
    print("Selected Candidate ID =", get_id)
    if get_id is not None:
        print('inside if part')
        # object = candidate_application.objects.filter(id=get_id).values()
        object = candidate_application.objects.get(id=get_id)
        print(object)
        # To store the same data of candidate application into the selected candidate database
        selected_candidate = selected_candidate_interview(your_name=object.your_name, email=object.email,
                                                          contact_no=object.mobile_number, department=object.department,
                                                          resume=object.resume, position=object.position,
                                                          current_ctc=object.current_ctc,
                                                          expected_ctc=object.expected_ctc)
        # To check the candidate already exist in the database or not
        x = selected_candidate_interview.objects.filter(your_name=object.your_name).count()
        print('This is the value of x==', x)
        if x:
            print('Candidate Already Exist')
            pass
        else:
            selected_candidate.save()
            print('Candidate added in database ')
        all_objects = selected_candidate_interview.objects.all().values()
        context = {'all_objects': all_objects}
        return render(request, 'HR/selected_candidate.html', context)


    else:
        all_objects = selected_candidate_interview.objects.all().values()
        context = {'all_objects': all_objects}
        return render(request, 'HR/selected_candidate.html', context)



@login_required
def all_selected_candidate(request):
    print("Inside selected candidate function")
    all_objects = selected_candidate_interview.objects.all().values()  # query to get all selected candidate for interview
    context = {'all_objects': all_objects,
               }
    return render(request, 'HR/selected_candidate.html', context)


from django.core.mail import EmailMultiAlternatives
import datetime


# Function for schedulingf the interview
@csrf_exempt
@login_required
def interview_schedule(request, id):
    # records_from_model_a = optional_interviewer_bank.objects.all()
    # Query to get unnique department in the table
    # department = optional_interviewer_bank.objects.values_list('department', flat=True).distinct()
    # query to get employee names wherer department is HR
    # employee_names_hr = optional_interviewer_bank.objects.filter(department='DEVELOPMENT').values_list('employee_name',flat=True)
    # employee_names_rfc_dev = optional_interviewer_bank.objects.filter(department='RFC DEVELOPMENT').values_list('employee_name', flat=True)
    # print('======',employee_names_rfc_dev)
    interviewers = total_interviewer_bank.objects.all()
    # print('these are ==',interviewers)

    get_id = id
    if get_id is not None and request.method == 'GET':  # When the id is present
        print('Id =', get_id)
        # Getting the data of single candidate
        object = selected_candidate_interview.objects.filter(id=get_id).values()
        print("Inside interview schedule object", object)
        context = {
            'object': object,
            'interviewers': interviewers,
        }
        return render(request, 'HR/Send_Mail_To_Candidate.html', context)

    elif request.method == 'POST':
        # Code to send mail
        print("post method is called ")
        name = request.POST['name']
        email = request.POST['email']
        contact_no = request.POST['contact']
        interviewer = request.POST['interviewer']
        mode = request.POST['mode']
        google_meet_link = request.POST['link']
        department = request.POST['department']
        position = request.POST['position']
        date = request.POST['date']
        time = request.POST['time']
        round = request.POST['round']
        interviewer_mail_query = total_interviewer_bank.objects.get(employee_name=interviewer)
        interviewer_mail = interviewer_mail_query.email

        # interviewer_email=optional_interviewer_bank.objects.filter(employee_name='employee_names_hr').values('email')
        # interviewer_email = optional_interviewer_bank.objects.get(employee_name=interviewer)

        print(name)
        print(email)
        print(contact_no)
        print(mode)
        print(google_meet_link)
        print(date)
        print(department)
        print(position)
        print(time)
        print("Selected Interviewer Name", interviewer)
        print("Interviewer Mail", interviewer_mail)

        data = scheduled_interview(name=name, email=email, contact_no=contact_no, mode=mode,
                                   google_meet_link=google_meet_link, date=date, time=time, department=department,
                                   round=round,position=position
                                   )

        data.save()

        print('Sending the Mail......')
        if mode == 'Online':
            # #this will send mail to candidate
            # subject, from_email, to = 'Interview Scheduled ', 'prathameshbhuskade.pr17@gmail.com', interviewer_mail
            # text_content = 'This is an important message.'
            # html_content = f'Dear {name},<br><br>Thank you for applying for the position with MasterSoft ERP Solutions. <br><br>We would like to join the online interview for the position. Your interview link and details are mentioned below : <br>{google_meet_link}<br>, <br>Please call me at (HR Contact Number) or email me at hr@iitms.co.in if you have any questions or need to reschedule. <br><br>Sincerely, <br><br>(Name Of Hr shd be fethched from login)<br>(Post Of Hr shd be fethched from login)<br><strong><br>MasterSoft ERP Solutions Plot No. 8B-1,<br> Sector 21 Non-SEZ, near Moraj, <br> Mihan, Khapri, Maharashtra 441108 <br>084480 10216</strong>'
            # msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            # msg.attach_alternative(html_content, "text/html")
            # msg.send()

            if interviewer_mail is not None:
                # subject, from_email, to = 'Interview Scheduled ', 'prathameshbhuskade.pr17@gmail.com', interviewer_mail
                # text_content = 'This is an important message.'
                # html_content = f'Dear {name},<br><br>I hope this email finds you well. As per our discussion on the phone, I am writing to inform you about the scheduled interview at Mastersoft.<br><br>The interview is scheduled for {date} at {time} and will be conducted via Online Mode.<br><br>The interview link is given below.<br> .Please be available on  the time of Interview.<br><br>Link : {google_meet_link} <Br><br>Sincerely,<br>HR'
                # msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                # msg.attach_alternative(html_content, "text/html")
                # msg.send()

                print("Mail send to interviewer for online mode")
            return render(request, 'HR/selected_candidate.html')


        elif mode == 'Offline':
            ## Google meet link with mail
            # subject, from_email, to = 'Interview Scheduled ', 'prathameshbhuskade.pr17@gmail.com', email
            # text_content = 'This is an important message.'
            # html_content = f'Dear {name},<br><br>Thank you for applying for the position in MasterSoft ERP Solutions.<br><p>We would like to invite you for the interview at our office.<br> Your interview details are given below : <br> Date:{date} At {time}, at MasterSoft ERP Solutions head office.<br>Address: Plot No. 8B-1, Sector 21 Non-SEZ, Near Moraj, Mihan, Khapri, Maharashtra 441108<p><p> Please be present at the venue 15 min before the given time along with  2 copies of Resume and concerned documents. Please keep the originals with you.<br> For any quires please call me at (HR Contact Number) or email me at hr@iitms.co.in if you need to reschedule. <p>Sincerely,<br>(Name Of Hr shd be fetched from login)<br>(Post Of Hr shd be fetched from login)<br><p><p><strong>MasterSoft ERP Solutions, Plot No. 8B-1,<br> Sector 21 Non-SEZ,Near Moraj,<br> Mihan, Khapri,Maharashtra 441108<br>084480 10216</strong>'
            # msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            # msg.attach_alternative(html_content, "text/html")
            # msg.send()
            if interviewer_mail is not None:
                # subject, from_email, to = 'Interview Scheduled ', 'prathameshbhuskade.pr17@gmail.com', email
                # text_content = 'This is an important message.'
                # html_content = f'Dear {name},<br><br>I hope this email finds you well. As per our discussion on the phone, I am writing to inform you about the scheduled interview at Mastersoft.<br><br>The interview is scheduled for {date} at {time} and will be conducted via Online Mode.<br><br>The interview link is given below.<br> .Please be available on  the time of Interview.<br><br><Br><br>Sincerely,<br>HR'
                # msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                # msg.attach_alternative(html_content, "text/html")
                # msg.send()
                print("Mail send to interviewer for offline mode")
                return redirect(all_selected_candidate)
        else:
            print('No mode selected')
            return HttpResponse('Interview mode not selected. Please re-submit the form properly')

        # subject, from_email, to = 'Interview Schemd duled ', 'prathameshbhuskade.pr17@gmail.com', 'prathameshbhuskade.pr17@gmail.com'
        # text_content = 'This is an important message.'
        # html_content = '<p>Hello, Your <strong>interview</strong>has been scheduled.</p>'
        # msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        # msg.attach_alternative(html_content, "text/html")
        # msg.send()

        # send_mail(
        #     'Testing',
        #     'Testing the mail function',      # Message or Mail Body
        #     'prathameshbhuskade.pr17@gmail.com',  # Sender of the mail
        #     ['prathameshbhuskade.pr17@gmail.com',],
        #
        #     fail_silently=False
        # )

        print('Form Submitted and mail was send ')
        return render(request, 'HR/selected_candidate.html')


# Function for Scheduling the second round of the candidate
@csrf_exempt
@login_required
def round_two_interview_scheduling(request, id):

    interviewers = total_interviewer_bank.objects.all()      # To get all the objects from Interviewers bank
    edit_entry = scheduled_interview.objects.get(id=id)

    get_id = id
    print('Id for 2nd round of the interview  ',get_id)
    if get_id is not None and request.method == 'GET':  # When the id is present
        print('Id =', get_id)
        # Getting the data of single candidate
        scheduled_interview_object = scheduled_interview.objects.filter(id=get_id).values()
        print("Inside Interview round tow scheduling function ", scheduled_interview_object)
        context = {
            'scheduled_interview_object': scheduled_interview_object,
            'interviewers': interviewers,
        }
        return render(request, 'HR/Send_Mail_To_Candidate_2.html', context)

    elif request.method == 'POST':
        # Code to send mail
        print("post method is called ")
        name = request.POST.get('name')
        email = request.POST.get('email')
        contact_no = request.POST.get('contact')
        interviewer = request.POST.get('interviewer')
        mode = request.POST.get('mode')
        google_meet_link = request.POST.get('link')
        department = request.POST.get('department')
        position = request.POST.get('position')
        date = request.POST.get('date')
        time = request.POST.get('time')
        round = request.POST.get('round')
        round_two = request.POST.get('round_two')
        machine_test = request.POST.get('machine_test')
        hr_round = request.POST.get('hr_round')
        interviewer_mail_query = total_interviewer_bank.objects.get(employee_name=interviewer)
        interviewer_mail = interviewer_mail_query.email

        # interviewer_email=optional_interviewer_bank.objects.filter(employee_name='employee_names_hr').values('email')
        # interviewer_email = optional_interviewer_bank.objects.get(employee_name=interviewer)

        print(name)
        print(email)
        print(contact_no)
        print(mode)
        print(google_meet_link)
        print(date)
        print(department)
        print(position)
        print(time)
        print("Selected Interviewer Name", interviewer)
        print("Interviewer Mail", interviewer_mail)

        scheduled_interview.objects.filter(id=id).update(name=name, email=email, contact_no=contact_no, mode=mode,google_meet_link=google_meet_link, date=date, time=time, department=department,round_two=round_two,position=position)


        # data = scheduled_interview(name=name, email=email, contact_no=contact_no, mode=mode,
        #                            google_meet_link=google_meet_link, date=date, time=time, department=department,
        #                            round_two=round_two,position=position
        #                            )

        #data.save()

        print('Sending the Mail......')
        if mode == 'Online':
            # #this will send mail to candidate
            # subject, from_email, to = 'Interview Scheduled ', 'prathameshbhuskade.pr17@gmail.com', interviewer_mail
            # text_content = 'This is an important message.'
            # html_content = f'Dear {name},<br><br>Thank you for applying for the position with MasterSoft ERP Solutions. <br><br>We would like to join the online interview for the position. Your interview link and details are mentioned below : <br>{google_meet_link}<br>, <br>Please call me at (HR Contact Number) or email me at hr@iitms.co.in if you have any questions or need to reschedule. <br><br>Sincerely, <br><br>(Name Of Hr shd be fethched from login)<br>(Post Of Hr shd be fethched from login)<br><strong><br>MasterSoft ERP Solutions Plot No. 8B-1,<br> Sector 21 Non-SEZ, near Moraj, <br> Mihan, Khapri, Maharashtra 441108 <br>084480 10216</strong>'
            # msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            # msg.attach_alternative(html_content, "text/html")
            # msg.send()

            if interviewer_mail is not None:
                # subject, from_email, to = 'Interview Scheduled ', 'prathameshbhuskade.pr17@gmail.com', interviewer_mail
                # text_content = 'This is an important message.'
                # html_content = f'Dear {name},<br><br>I hope this email finds you well. As per our discussion on the phone, I am writing to inform you about the scheduled interview at Mastersoft.<br><br>The interview is scheduled for {date} at {time} and will be conducted via Online Mode.<br><br>The interview link is given below.<br> .Please be available on  the time of Interview.<br><br>Link : {google_meet_link} <Br><br>Sincerely,<br>HR'
                # msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                # msg.attach_alternative(html_content, "text/html")
                # msg.send()
                print("Mail send to interviewer for online mode")
                return redirect(scheduled_interviews)
            return render(request, 'HR/selected_candidate.html')


        elif mode == 'Offline':
            ## Google meet link with mail
            # subject, from_email, to = 'Interview Scheduled ', 'prathameshbhuskade.pr17@gmail.com', email
            # text_content = 'This is an important message.'
            # html_content = f'Dear {name},<br><br>Thank you for applying for the position in MasterSoft ERP Solutions.<br><p>We would like to invite you for the interview at our office.<br> Your interview details are given below : <br> Date:{date} At {time}, at MasterSoft ERP Solutions head office.<br>Address: Plot No. 8B-1, Sector 21 Non-SEZ, Near Moraj, Mihan, Khapri, Maharashtra 441108<p><p> Please be present at the venue 15 min before the given time along with  2 copies of Resume and concerned documents. Please keep the originals with you.<br> For any quires please call me at (HR Contact Number) or email me at hr@iitms.co.in if you need to reschedule. <p>Sincerely,<br>(Name Of Hr shd be fetched from login)<br>(Post Of Hr shd be fetched from login)<br><p><p><strong>MasterSoft ERP Solutions, Plot No. 8B-1,<br> Sector 21 Non-SEZ,Near Moraj,<br> Mihan, Khapri,Maharashtra 441108<br>084480 10216</strong>'
            # msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            # msg.attach_alternative(html_content, "text/html")
            # msg.send()
            if interviewer_mail is not None:
                # subject, from_email, to = 'Interview Scheduled ', 'prathameshbhuskade.pr17@gmail.com', email
                # text_content = 'This is an important message.'
                # html_content = f'Dear {name},<br><br>I hope this email finds you well. As per our discussion on the phone, I am writing to inform you about the scheduled interview at Mastersoft.<br><br>The interview is scheduled for {date} at {time} and will be conducted via Online Mode.<br><br>The interview link is given below.<br> .Please be available on  the time of Interview.<br><br><Br><br>Sincerely,<br>HR'
                # msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                # msg.attach_alternative(html_content, "text/html")
                # msg.send()
                print("Mail send to interviewer for offline mode")
                return redirect(scheduled_interviews)
        else:
            print('No mode selected')
            return HttpResponse('Interview mode not selected. Please re-submit the form properly')

        # subject, from_email, to = 'Interview Schemd duled ', 'prathameshbhuskade.pr17@gmail.com', 'prathameshbhuskade.pr17@gmail.com'
        # text_content = 'This is an important message.'
        # html_content = '<p>Hello, Your <strong>interview</strong>has been scheduled.</p>'
        # msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        # msg.attach_alternative(html_content, "text/html")
        # msg.send()

        # send_mail(
        #     'Testing',
        #     'Testing the mail function',      # Message or Mail Body
        #     'prathameshbhuskade.pr17@gmail.com',  # Sender of the mail
        #     ['prathameshbhuskade.pr17@gmail.com',],
        #
        #     fail_silently=False
        # )

        print('Form Submitted and mail was send ')
        return render(request, 'HR/selected_candidate.html')


#Function for Scheduling the third round of the candidate
@csrf_exempt
@login_required
def round_three_machine_test_scheduling(request, id):

    interviewers = total_interviewer_bank.objects.all()      # To get all the objects from Interviewers bank

    get_id = id
    print('Id for 2nd round of the interview  ',get_id)
    if get_id is not None and request.method == 'GET':  # When the id is present
        print('Id =', get_id)
        # Getting the data of single candidate
        scheduled_interview_object = scheduled_interview.objects.filter(id=get_id).values()
        print("Inside Interview round tow scheduling function ", scheduled_interview_object)
        context = {
            'scheduled_interview_object': scheduled_interview_object,
            'interviewers': interviewers,
        }
        return render(request, 'HR/Send_Mail_To_Candidate_3.html', context)

    elif request.method == 'POST':
        # Code to send mail
        print("post method is called ")
        name = request.POST['name']
        email = request.POST['email']
        contact_no = request.POST['contact']
        interviewer = request.POST['interviewer']
        mode = request.POST['mode']
        google_meet_link = request.POST['link']
        department = request.POST['department']
        position = request.POST['position']
        date = request.POST['date']
        time = request.POST['time']
        round = request.POST['round']
        round_two = request.POST['round_two']
        machine_test = request.POST['machine_test']
        hr_round = request.POST['hr_round']
        interviewer_mail_query = total_interviewer_bank.objects.get(employee_name=interviewer)
        interviewer_mail = interviewer_mail_query.email

        # interviewer_email=optional_interviewer_bank.objects.filter(employee_name='employee_names_hr').values('email')
        # interviewer_email = optional_interviewer_bank.objects.get(employee_name=interviewer)

        print(name)
        print(email)
        print(contact_no)
        print(mode)
        print(google_meet_link)
        print(date)
        print(department)
        print(position)
        print(time)
        print("Selected Interviewer Name", interviewer)
        print("Interviewer Mail", interviewer_mail)

        scheduled_interview.objects.filter(id=id).update(name=name, email=email, contact_no=contact_no, mode=mode,
                                                         google_meet_link=google_meet_link, date=date, time=time,
                                                         department=department, machine_test=machine_test, position=position)

        # data = scheduled_interview(name=name, email=email, contact_no=contact_no, mode=mode,
        #                            google_meet_link=google_meet_link, date=date, time=time, department=department,
        #                            machine_test=machine_test,position=position
        #                            )
        #
        # data.save()

        print('Sending the Mail......')
        if mode == 'Online':
            # #this will send mail to candidate
            # subject, from_email, to = 'Interview Scheduled ', 'prathameshbhuskade.pr17@gmail.com', interviewer_mail
            # text_content = 'This is an important message.'
            # html_content = f'Dear {name},<br><br>Thank you for applying for the position with MasterSoft ERP Solutions. <br><br>We would like to join the online interview for the position. Your interview link and details are mentioned below : <br>{google_meet_link}<br>, <br>Please call me at (HR Contact Number) or email me at hr@iitms.co.in if you have any questions or need to reschedule. <br><br>Sincerely, <br><br>(Name Of Hr shd be fethched from login)<br>(Post Of Hr shd be fethched from login)<br><strong><br>MasterSoft ERP Solutions Plot No. 8B-1,<br> Sector 21 Non-SEZ, near Moraj, <br> Mihan, Khapri, Maharashtra 441108 <br>084480 10216</strong>'
            # msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            # msg.attach_alternative(html_content, "text/html")
            # msg.send()

            if interviewer_mail is not None:
                # subject, from_email, to = 'Interview Scheduled ', 'prathameshbhuskade.pr17@gmail.com', interviewer_mail
                # text_content = 'This is an important message.'
                # html_content = f'Dear {name},<br><br>I hope this email finds you well. As per our discussion on the phone, I am writing to inform you about the scheduled interview at Mastersoft.<br><br>The interview is scheduled for {date} at {time} and will be conducted via Online Mode.<br><br>The interview link is given below.<br> .Please be available on  the time of Interview.<br><br>Link : {google_meet_link} <Br><br>Sincerely,<br>HR'
                # msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                # msg.attach_alternative(html_content, "text/html")
                # msg.send()
                print("Mail send to interviewer for online mode")
                return redirect(scheduled_interviews)
            return render(request, 'HR/selected_candidate_3.html')


        elif mode == 'Offline':
            ## Google meet link with mail
            # subject, from_email, to = 'Interview Scheduled ', 'prathameshbhuskade.pr17@gmail.com', email
            # text_content = 'This is an important message.'
            # html_content = f'Dear {name},<br><br>Thank you for applying for the position in MasterSoft ERP Solutions.<br><p>We would like to invite you for the interview at our office.<br> Your interview details are given below : <br> Date:{date} At {time}, at MasterSoft ERP Solutions head office.<br>Address: Plot No. 8B-1, Sector 21 Non-SEZ, Near Moraj, Mihan, Khapri, Maharashtra 441108<p><p> Please be present at the venue 15 min before the given time along with  2 copies of Resume and concerned documents. Please keep the originals with you.<br> For any quires please call me at (HR Contact Number) or email me at hr@iitms.co.in if you need to reschedule. <p>Sincerely,<br>(Name Of Hr shd be fetched from login)<br>(Post Of Hr shd be fetched from login)<br><p><p><strong>MasterSoft ERP Solutions, Plot No. 8B-1,<br> Sector 21 Non-SEZ,Near Moraj,<br> Mihan, Khapri,Maharashtra 441108<br>084480 10216</strong>'
            # msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            # msg.attach_alternative(html_content, "text/html")
            # msg.send()
            if interviewer_mail is not None:
                # subject, from_email, to = 'Interview Scheduled ', 'prathameshbhuskade.pr17@gmail.com', email
                # text_content = 'This is an important message.'
                # html_content = f'Dear {name},<br><br>I hope this email finds you well. As per our discussion on the phone, I am writing to inform you about the scheduled interview at Mastersoft.<br><br>The interview is scheduled for {date} at {time} and will be conducted via Online Mode.<br><br>The interview link is given below.<br> .Please be available on  the time of Interview.<br><br><Br><br>Sincerely,<br>HR'
                # msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                # msg.attach_alternative(html_content, "text/html")
                # msg.send()
                print("Mail send to interviewer for offline mode")
                return redirect(scheduled_interviews)
        else:
            print('No mode selected')
            return HttpResponse('Interview mode not selected. Please re-submit the form properly')

        # subject, from_email, to = 'Interview Schemd duled ', 'prathameshbhuskade.pr17@gmail.com', 'prathameshbhuskade.pr17@gmail.com'
        # text_content = 'This is an important message.'
        # html_content = '<p>Hello, Your <strong>interview</strong>has been scheduled.</p>'
        # msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        # msg.attach_alternative(html_content, "text/html")
        # msg.send()

        # send_mail(
        #     'Testing',
        #     'Testing the mail function',      # Message or Mail Body
        #     'prathameshbhuskade.pr17@gmail.com',  # Sender of the mail
        #     ['prathameshbhuskade.pr17@gmail.com',],
        #
        #     fail_silently=False
        # )

        print('Form Submitted and mail was send ')
        return render(request, 'HR/selected_candidate_3.html')


# Function for scheduling the HR round of the candidate
@csrf_exempt
@login_required
def round_four_hr_round_scheduling(request, id):

    interviewers = total_interviewer_bank.objects.all()      # To get all the objects from Interviewers bank

    get_id = id
    print('Id for 2nd round of the interview  ',get_id)
    if get_id is not None and request.method == 'GET':  # When the id is present
        print('Id =', get_id)
        # Getting the data of single candidate
        scheduled_interview_object = scheduled_interview.objects.filter(id=get_id).values()
        print("Inside Interview round tow scheduling function ", scheduled_interview_object)
        context = {
            'scheduled_interview_object': scheduled_interview_object,
            'interviewers': interviewers,
        }
        return render(request, 'HR/Send_Mail_To_Candidate_4.html', context)

    elif request.method == 'POST':
        # Code to send mail
        print("post method is called ")
        name = request.POST['name']
        email = request.POST['email']
        contact_no = request.POST['contact']
        interviewer = request.POST['interviewer']
        mode = request.POST['mode']
        google_meet_link = request.POST['link']
        department = request.POST['department']
        position = request.POST['position']
        date = request.POST['date']
        time = request.POST['time']
        round = request.POST['round']
        round_two = request.POST['round_two']
        machine_test = request.POST['machine_test']
        hr_round = request.POST['hr_round']
        interviewer_mail_query = total_interviewer_bank.objects.get(employee_name=interviewer)
        interviewer_mail = interviewer_mail_query.email

        # interviewer_email=optional_interviewer_bank.objects.filter(employee_name='employee_names_hr').values('email')
        # interviewer_email = optional_interviewer_bank.objects.get(employee_name=interviewer)

        print(name)
        print(email)
        print(contact_no)
        print(mode)
        print(google_meet_link)
        print(date)
        print(department)
        print(position)
        print(time)
        print("Selected Interviewer Name", interviewer)
        print("Interviewer Mail", interviewer_mail)

        scheduled_interview.objects.filter(id=id).update(name=name, email=email, contact_no=contact_no, mode=mode,
                                                         google_meet_link=google_meet_link, date=date, time=time,
                                                         department=department, hr_round=hr_round,
                                                         position=position)

        # data = scheduled_interview(name=name, email=email, contact_no=contact_no, mode=mode,
        #                            google_meet_link=google_meet_link, date=date, time=time, department=department,
        #                            hr_round=hr_round,position=position
        #                            )
        #
        # data.save()

        print('Sending the Mail......')
        if mode == 'Online':
            # #this will send mail to candidate
            # subject, from_email, to = 'Interview Scheduled ', 'prathameshbhuskade.pr17@gmail.com', interviewer_mail
            # text_content = 'This is an important message.'
            # html_content = f'Dear {name},<br><br>Thank you for applying for the position with MasterSoft ERP Solutions. <br><br>We would like to join the online interview for the position. Your interview link and details are mentioned below : <br>{google_meet_link}<br>, <br>Please call me at (HR Contact Number) or email me at hr@iitms.co.in if you have any questions or need to reschedule. <br><br>Sincerely, <br><br>(Name Of Hr shd be fethched from login)<br>(Post Of Hr shd be fethched from login)<br><strong><br>MasterSoft ERP Solutions Plot No. 8B-1,<br> Sector 21 Non-SEZ, near Moraj, <br> Mihan, Khapri, Maharashtra 441108 <br>084480 10216</strong>'
            # msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            # msg.attach_alternative(html_content, "text/html")
            # msg.send()

            if interviewer_mail is not None:
                # subject, from_email, to = 'Interview Scheduled ', 'prathameshbhuskade.pr17@gmail.com', interviewer_mail
                # text_content = 'This is an important message.'
                # html_content = f'Dear {name},<br><br>I hope this email finds you well. As per our discussion on the phone, I am writing to inform you about the scheduled interview at Mastersoft.<br><br>The interview is scheduled for {date} at {time} and will be conducted via Online Mode.<br><br>The interview link is given below.<br> .Please be available on  the time of Interview.<br><br>Link : {google_meet_link} <Br><br>Sincerely,<br>HR'
                # msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                # msg.attach_alternative(html_content, "text/html")
                # msg.send()

                print("Mail send to interviewer for online mode")
                return redirect(scheduled_interviews)
            return render(request, 'HR/selected_candidate_4.html')


        elif mode == 'Offline':
            ## Google meet link with mail
            # subject, from_email, to = 'Interview Scheduled ', 'prathameshbhuskade.pr17@gmail.com', email
            # text_content = 'This is an important message.'
            # html_content = f'Dear {name},<br><br>Thank you for applying for the position in MasterSoft ERP Solutions.<br><p>We would like to invite you for the interview at our office.<br> Your interview details are given below : <br> Date:{date} At {time}, at MasterSoft ERP Solutions head office.<br>Address: Plot No. 8B-1, Sector 21 Non-SEZ, Near Moraj, Mihan, Khapri, Maharashtra 441108<p><p> Please be present at the venue 15 min before the given time along with  2 copies of Resume and concerned documents. Please keep the originals with you.<br> For any quires please call me at (HR Contact Number) or email me at hr@iitms.co.in if you need to reschedule. <p>Sincerely,<br>(Name Of Hr shd be fetched from login)<br>(Post Of Hr shd be fetched from login)<br><p><p><strong>MasterSoft ERP Solutions, Plot No. 8B-1,<br> Sector 21 Non-SEZ,Near Moraj,<br> Mihan, Khapri,Maharashtra 441108<br>084480 10216</strong>'
            # msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            # msg.attach_alternative(html_content, "text/html")
            # msg.send()
            if interviewer_mail is not None:
                # subject, from_email, to = 'Interview Scheduled ', 'prathameshbhuskade.pr17@gmail.com', email
                # text_content = 'This is an important message.'
                # html_content = f'Dear {name},<br><br>I hope this email finds you well. As per our discussion on the phone, I am writing to inform you about the scheduled interview at Mastersoft.<br><br>The interview is scheduled for {date} at {time} and will be conducted via Online Mode.<br><br>The interview link is given below.<br> .Please be available on  the time of Interview.<br><br><Br><br>Sincerely,<br>HR'
                # msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                # msg.attach_alternative(html_content, "text/html")
                # msg.send()
                print("Mail send to interviewer for offline mode")
                return redirect(scheduled_interviews)
        else:
            print('No mode selected')
            return HttpResponse('Interview mode not selected. Please re-submit the form properly')

        # subject, from_email, to = 'Interview Schemd duled ', 'prathameshbhuskade.pr17@gmail.com', 'prathameshbhuskade.pr17@gmail.com'
        # text_content = 'This is an important message.'
        # html_content = '<p>Hello, Your <strong>interview</strong>has been scheduled.</p>'
        # msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        # msg.attach_alternative(html_content, "text/html")
        # msg.send()

        # send_mail(
        #     'Testing',
        #     'Testing the mail function',      # Message or Mail Body
        #     'prathameshbhuskade.pr17@gmail.com',  # Sender of the mail
        #     ['prathameshbhuskade.pr17@gmail.com',],
        #
        #     fail_silently=False
        # )

        print('Form Submitted and mail was send ')
        return render(request, 'HR/selected_candidate_4.html')



# -----------Backup Code----------------------

# Function for scheduling interview and sending the mail to selected candidate
# @csrf_exempt
# def interview_schedule(request, id):
#     records_from_model_a = optional_interviewer_bank.objects.all()
#     print(records_from_model_a)
#     get_id = id
#     if get_id is not None and request.method == 'GET':  # When the id is present
#         print('Id =',get_id)
#         # Getting the data of single candidate
#         object = selected_candidate_interview.objects.filter(id=get_id).values()
#         print("Inside interview schedule object", object)
#         context = {
#             'object': object,
#             'records_from_model_a':records_from_model_a
#                    }
#         return render(request, 'HR/Send_Mail_To_Candidate.html', context)
#
#     elif request.method == 'POST':
#
#
#         # Code to send mail
#
#         name = request.POST['name']
#         email = request.POST['email']
#         contact_no = request.POST['contact']
#         mode = request.POST['mode']
#         google_meet_link = request.POST['link']
#         department = request.POST['department']
#         date = request.POST['date']
#         time = request.POST['time']
#
#         print(name)
#         print(email)
#         print(contact_no)
#         print(mode)
#         print(google_meet_link)
#         print(date)
#         print(department)
#         print(time)
#
#         data = scheduled_interview(name=name,email=email,contact_no=contact_no,mode=mode,
#                         google_meet_link=google_meet_link,date=date,time=time,department=department
#                         )
#
#         data.save()
#
#         print('Sending the Mail......')
#         if mode == 'Online':
#             subject, from_email, to = 'Interview Scheduled ', 'prathameshbhuskade.pr17@gmail.com', email
#             text_content = 'This is an important message.'
#             html_content = f'Dear {name},<br><br>Thank you for applying for the position with MasterSoft ERP Solutions. <br><br>We would like to join the online interview for the position. Your interview link and details are mentioned below : <br>{google_meet_link}<br>, <br>Please call me at (HR Contact Number) or email me at hr@iitms.co.in if you have any questions or need to reschedule. <br><br>Sincerely, <br><br>(Name Of Hr shd be fethched from login)<br>(Post Of Hr shd be fethched from login)<br><strong><br>MasterSoft ERP Solutions Plot No. 8B-1,<br> Sector 21 Non-SEZ, near Moraj, <br> Mihan, Khapri, Maharashtra 441108 <br>084480 10216</strong>'
#             msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
#             msg.attach_alternative(html_content, "text/html")
#             msg.send()
#             return render(request,'HR/selected_candidate.html')
#
#         elif mode == 'Offline':
#             # Google meet link with mail
#             subject, from_email, to = 'Interview Scheduled ', 'prathameshbhuskade.pr17@gmail.com', email
#             text_content = 'This is an important message.'
#             html_content = f'Dear {name},<br><br>Thank you for applying for the position in MasterSoft ERP Solutions.<br><p>We would like to invite you for the interview at our office.<br> Your interview details are given below : <br> Date:{date} At {time}, at MasterSoft ERP Solutions head office.<br>Address: Plot No. 8B-1, Sector 21 Non-SEZ, Near Moraj, Mihan, Khapri, Maharashtra 441108<p><p> Please be present at the venue 15 min before the given time along with  2 copies of Resume and concerned documents. Please keep the originals with you.<br> For any quires please call me at (HR Contact Number) or email me at hr@iitms.co.in if you need to reschedule. <p>Sincerely,<br>(Name Of Hr shd be fetched from login)<br>(Post Of Hr shd be fetched from login)<br><p><p><strong>MasterSoft ERP Solutions, Plot No. 8B-1,<br> Sector 21 Non-SEZ,Near Moraj,<br> Mihan, Khapri,Maharashtra 441108<br>084480 10216</strong>'
#             msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
#             msg.attach_alternative(html_content, "text/html")
#             msg.send()
#         else:
#             print('No mode selected')
#             return HttpResponse('Interview mode not selected. Please re-submit the form properly')
#
#
#
#         # subject, from_email, to = 'Interview Schemd duled ', 'prathameshbhuskade.pr17@gmail.com', 'prathameshbhuskade.pr17@gmail.com'
#         # text_content = 'This is an important message.'
#         # html_content = '<p>Hello, Your <strong>interview</strong>has been scheduled.</p>'
#         # msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
#         # msg.attach_alternative(html_content, "text/html")
#         # msg.send()
#
#         # send_mail(
#         #     'Testing',
#         #     'Testing the mail function',      # Message or Mail Body
#         #     'prathameshbhuskade.pr17@gmail.com',  # Sender of the mail
#         #     ['prathameshbhuskade.pr17@gmail.com',],
#         #
#         #     fail_silently=False
#         # )
#
#         print('Form Submitted and mail was send ')
#         return render(request, 'HR/selected_candidate.html')


# def show_data(request):
#     students = Student.objects.all()
#     for student in students:
#         candidate = Candidate(name=student.name, age=student.age, political_party='Independent')
#         candidate.save()
#     return render(request, 'success.html')


def test(request):
    if request.method == 'POST':
        print('inside the test function ')
        department = request.POST['department']
        position = request.POST['position']
        data = test_model(department=department, position=position)
        data.save()
        print('saved to database')
        return render(request, "test.html")
    return render(request, "test.html")


@login_required
def scheduled_interviews(request):
    scheduled_interview_all_object = scheduled_interview.objects.all().values()  # query to get all scheduled
    context = {
               'scheduled_interview_all_object': scheduled_interview_all_object
               }
    return render(request, 'HR/scheduled_interview.html', context)




#-----------------------------------------------------------------------------------------------------------------------
from django.shortcuts import render
from docxtpl import DocxTemplate
from datetime import date
import calendar
from docx2pdf import convert

# Function to generate offer letter of the candidate....It will be called on generate offer letter button in scheduked interview.html.
def generate_offer_letter(request,id):
    get_id = id            # get the row id from generate offer letter button.
    # query to get the data by Id

    if request.method == 'GET'and get_id:
        data = scheduled_interview.objects.filter(id=get_id).values()
        context = {
            'data': data
        }
        return render(request,'HR/generate_offer_letter.html',context)

    elif request.method == 'POST' and get_id:


        # Date Time section
        d = date.today().strftime('%d ')
        test_num = date.today().strftime('%m')
        mnt = int(test_num)
        m = calendar.month_name[mnt]
        y = date.today().strftime(' %Y')

        # input Section (This information)
        name = request.POST.get("name")
        designation = request.POST.get("designation")
        position = request.POST.get("position")
        joining_date = request.POST.get("joining_date")
        package = request.POST.get("package")
        in_words = request.POST.get("in_words")
        location = request.POST.get("location")

        print('Form data=',name,designation,position,joining_date,package,location)


        # shows Replacements to be done on the documents.
        change = {
                  'name': name,
                  'designation': designation,
                  'position': position,
                  'package': package,
                  'joining_date': joining_date,
                  'location': location,
                   'in_words': in_words,
                  }

        # path to document
        tpl = DocxTemplate('Offer_Nagpur.docx.')

        # Replace
        tpl.render(change)

        # save the document
        docName = name + "_Offer_Letter.doc"
        tpl.save(docName)

        # doc = aw.Document(docName)
        # doc.save(name+".pdf")
        # doc.save('Offer_Letter'+name+'_'+designation+'.docx')
        # Converting it to PDF
        #convert(docName, "pdf")

        print("offer letter generated ")
        return redirect(scheduled_interviews)


# The function to view the resymer of the candidate
from django.http import FileResponse
def get_pdf(request, id):
    get_id = id
    file_object = selected_candidate_interview.objects.get(id=get_id)
    response = FileResponse(file_object.resume)
    return response

# function toview resume for applied candidate
def get_pdf2(request, id):
    get_id = id
    file_object = candidate_master.objects.get(id=get_id)
    response = FileResponse(file_object.resume)
    return response

# Function to show Candidate Master Table
def candidate_master_view(request):
    data = candidate_master.objects.all().values()
    context = {
            'data': data
        }

    return render(request, 'HR/candidate_master.html', context)

# Function to show Recruitment Master
def recruitment_master_view(request):
    data = recruitment_master.objects.all().values()
    context = {
            'data': data
        }
    return render(request, 'HR/recruitment_master.html', context)


#To remove the entry from the table selected candidate for interview this function will be called on remove button
def remove_selected_candidate_interview(request,id):
    if id is not None:
        obj = selected_candidate_interview.objects.get(id=id)
        obj.delete()
        return redirect('selected_applicants1')
    else:
        pass


#To remove the entry from the table Interview Scheduled Table for interview this function will be called on remove button
def remove_scheduled_interview(request,id):
    if id is not None:
        obj = scheduled_interview.objects.get(id=id)
        obj.delete()
        return redirect('')
    else:
        pass


