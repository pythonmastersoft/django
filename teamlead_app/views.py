import dataclasses

import datetime as datetime
import os

from docxtpl import DocxTemplate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.mail import send_mail, send_mass_mail, EmailMultiAlternatives
from datetime import datetime, date
from django.forms import FileField
from django.views import generic
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.models import User, Group
from datetime import datetime, timedelta, date
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect

import calendar
# from .models import requirement
from .models import *


# Create your views here.


# --------------- Creating decorators to check if the user belongs to the certain group or not ---------------------

def is_teamlead(user):
    return user.groups.filter(name='Team_Leads').exists()


def is_Human_Resource(user):
    return user.groups.filter(name='Human_Resource').exists()


def is_Administrator(user):
    return user.groups.filter(name='Administrator').exists()


#-------------------------------------------------------------------------------------------------------------------

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

def db_logout(request):
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
        # if requirement_raised.objects.all().values():
        #     all_requirement_raised = requirement_raised.objects.all().values()
        #     context = {'all_requirement_raised': all_requirement_raised}
        #     return render(request, 'HR/current_requirement.html', context)

        all_requirement_raised = requirement_raised.objects.all().values()
        context1 = {'all_requirement_raised': all_requirement_raised}
        if recruitment_master.objects.all().values():
            all_objects = recruitment_master.objects.all().values()
            context = {'all_objects': all_objects,'all_requirement_raised': all_requirement_raised}
            return render(request, 'HR/current_requirement.html', context)


        return render(request, 'HR/current_requirement.html',context1)

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

            # Requirement raised table when entry get updated it will be added in recruitement master
            data = requirement_raised(department=department,project_name=project_name,
                               position=position, type_of_resource=type_of_resource,
                               posting_location=posting_location, experience_required=experience_required,
                               special_remark=special_remark, technologies_required=technologies_required,
                               requestor_name=requestor_name, no_of_positions=no_of_positions)
            data.save()
            print("Sending Mail....")

           # Code for sending the mail
           #  send_mail(
           #      'Requiremnt Raised ',
           #      'tesing the mail function.',
           #      'python@iitms.co.in',#Sender of the mail
           #      ['prathameshbhuskade.pr17@gmail.com', 'prathameshbhuskade@gmail.com'],
           #      # HR Mail id and admin mail id (Reciever)
           #      fail_silently=False
           #  )

            print('Mail Send')
            return render(request, 'HR/home.html')

        return render(request, 'HR/home.html')

    else:
        print("You don't have access to HR View", request.user)
        return redirect('/login')


def approve_requirement(request,id):
    id=id
    if id is not None:
        # Copy the same entry form requirement_raised to recruitment_master table
        object_to_copy = requirement_raised.objects.get(id=id)
        new_object = recruitment_master()
        new_object.requestor_name = object_to_copy.requestor_name
        new_object.project_name = object_to_copy.project_name
        new_object.department = object_to_copy.department
        new_object.position = object_to_copy.position
        new_object.type_of_resource = object_to_copy.type_of_resource
        new_object.posting_location = object_to_copy.posting_location
        new_object.experience_required = object_to_copy.experience_required
        new_object.technologies_required = object_to_copy.technologies_required
        new_object.special_remark = object_to_copy.special_remark
        new_object.no_of_positions = object_to_copy.no_of_positions
        new_object.created_at = object_to_copy.created_at
        new_object.budget = object_to_copy.budget
        new_object.save()

        object_to_copy.delete()      # Deleting the entry after adding the same in the master
        print("Approved Button Clicked")
        return redirect(hr_view)
    return redirect(hr_view)

def reject_requirement(request,id):
    object_to_delete = requirement_raised.objects.get(id=id)
    object_to_delete.delete()
    print("Requirement Rejected ")

@login_required
def update_budget(request):
    return render('HR/current_requiremnet')


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

        data = requirement_raised(department=department, project_name=project_name,
                                  position=position, type_of_resource=type_of_resource,
                                  posting_location=posting_location, experience_required=experience_required,
                                  special_remark=special_remark, technologies_required=technologies_required,
                                  requestor_name=requestor_name, no_of_positions=no_of_positions)
        data.save()
        print("Entry Added ")
        print("Sending Mail....")

        # Code for sending the mail
        # send_mail(
        #     'Requiremnt Raised ',
        #     'tesing the mail function.',
        #     'prathameshbhuskade.pr17@gmail.com',  # Sender of the mail
        #     ['prathameshbhuskade.pr17@gmail.com', 'prathameshbhuskade@gmail.com'],
        #     # HR Mail id and admin mail id (Reciever)
        #     fail_silently=False
        # )

        # For sending the diffrent mails to the diffrent mail id
        # datatuple = (
        #         ('Subject', 'Message.', 'from@example.com', ['john@example.com']),
        #         ('Subject', 'Message.', 'from@example.com', ['jane@example.com']),
        #     )
        # send_mass_mail(datatuple)
        #
        print('Mail Send success')

        return render(request, 'teamlead/home.html',{'requestor_name': requestor_name })

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
        father_name = request.POST['email']
        permanent_address = request.POST['permanent_address']
        mobile_number = request.POST['mobile_number']
        years_of_experience = request.POST['years_of_experience']
        years_of_relevant_experience = request.POST['years_of_relevant_experience']
        current_ctc = request.POST['current_ctc']
        expected_ctc = request.POST['expected_ctc']
        resume = request.FILES['resume']
        department = request.POST['department']
        ready_to_relocate = request.POST.get('ready_to_relocate')
        position = request.POST.get('position')
        data = candidate_master(your_name=your_name, email=email, mobile_number=mobile_number,
                                     years_of_experience=years_of_experience, current_ctc=current_ctc,
                                     expected_ctc=expected_ctc,
                                     years_of_relevant_experience=years_of_relevant_experience,department=department,
                                     position=position, resume=resume,ready_to_relocate=ready_to_relocate,permanent_address=permanent_address,father_name=father_name)
        print("I am here")
        data.save()
        print("done")
        data = candidate_application(your_name=your_name, email=email, mobile_number=mobile_number,
                                years_of_experience=years_of_experience, current_ctc=current_ctc,
                                expected_ctc=expected_ctc,
                                years_of_relevant_experience=years_of_relevant_experience, department=department,
                                position=position, resume=resume, ready_to_relocate=ready_to_relocate,permanent_address=permanent_address,father_name=father_name)
        data.save()

        return render(request, 'HR/Apply Pages/apply.html')

    return render(request, 'HR/Apply Pages/apply.html')


@csrf_exempt
def document_upload_form(request):
    print("Inside upload function")
    if request.method == 'POST':
        print("post method called upload form ")
        name = request.POST.get('name')
        email = request.POST.get('email')
        mobile_number = request.POST.get('mobile_number')
        pancard = request.FILES['pancard']
        address_proof = request.FILES['address_proof']
        photo_identity_proof = request.FILES['photo_identity_proof']
        ssc_certificate = request.FILES['ssc_certificate']
        hsc_certificate = request.FILES['hsc_certificate']
        diploma_certificate = request.FILES['diploma_certificate']
        degree_certificate = request.FILES['degree_certificate']
        pg_certificate = request.FILES['pg_certificate']
        college_tc = request.FILES['college_tc']
        passport_size_photo = request.FILES['passport_size_photo']
        bank_passbook = request.FILES['bank_passbook']
        internship_certificate = request.FILES['internship_certificate']
        experience_certificate = request.FILES['experience_certificate']
        salary_slip = request.FILES['salary_slip']
        form_16 = request.FILES['form_16']
        passport = request.FILES['passport']
        covid_vaccination_certificate = request.FILES['covid_vaccination_certificate']
        medical_certificate = request.FILES['medical_certificate']
        police_verification_document = request.FILES['police_verification_document']
        data = upload_document(name=name,email=email,mobile_number=mobile_number,pancard=pancard,address_proof=address_proof,photo_identity_proof=photo_identity_proof,
                               ssc_certificate=ssc_certificate,hsc_certificate=hsc_certificate,diploma_certificate=diploma_certificate,degree_certificate=degree_certificate,
                               pg_certificate=pg_certificate,college_tc=college_tc,passport_size_photo=passport_size_photo,bank_passbook=bank_passbook,
                               internship_certificate=internship_certificate,experience_certificate=experience_certificate,salary_slip=salary_slip,
                               form_16=form_16,passport=passport,covid_vaccination_certificate=covid_vaccination_certificate,medical_certificate=medical_certificate,
                               police_verification_document=police_verification_document
                               )

        print("Uploaded Successfully")
        try:
            get_candidate = candidate_master.objects.get(email=email)
            candidate_id = get_candidate.id
            print("Entry found with same email address", candidate_id)
            update_masters = candidate_master.objects.filter(id=candidate_id).update(pancard=pancard,address_proof=address_proof,photo_identity_proof=photo_identity_proof,
                               ssc_certificate=ssc_certificate,hsc_certificate=hsc_certificate,diploma_certificate=diploma_certificate,degree_certificate=degree_certificate,
                               pg_certificate=pg_certificate,college_tc=college_tc,passport_size_photo=passport_size_photo,bank_passbook=bank_passbook,
                               internship_certificate=internship_certificate,experience_certificate=experience_certificate,salary_slip=salary_slip,
                               form_16=form_16,passport=passport,covid_vaccination_certificate=covid_vaccination_certificate,medical_certificate=medical_certificate,
                               police_verification_document=police_verification_document)

            data.save()
            print("Documents uploaded and saved in candidate master")
        except candidate_master.DoesNotExist:
            # If the code reaches here, it means no candidate with the given email exists
            print("Entry not found in Candidate Master")

        return render(request, 'Document_upload_from.html')

    return render(request, 'Document_upload_from.html')


#from teamlead_app.models import candidate_master
@login_required
@csrf_exempt
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

# from django.core.mail import EmailMultiAlternatives
# import datetime

# Function for scheduling the HR round of the candidate
@csrf_exempt
@login_required
def round_scheduling(request, id):
    print("Inside Scheduling interview")
    interviewers = total_interviewer_bank.objects.all()   # To get all the objects from Interviewers bank
    get_id = id
    print('Id for 2nd round of the interview ',get_id)
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
        interview_round = request.POST.get('interview_round')
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
        print(interview_round)
        print("Selected Interviewer Name", interviewer)
        print("Interviewer Mail", interviewer_mail)

        rows_updated=scheduled_interview.objects.filter(id=id).update(name=name, email=email, contact_no=contact_no, mode=mode,
                                                         google_meet_link=google_meet_link, date=date, time=time,
                                                         department=department, interview_round=interview_round,
                                                         position=position)


        if rows_updated > 0 and candidate_master.objects.filter(your_name=name, department=department).exists():
            try:
                candidate = candidate_master.objects.get(your_name=name, department=department)
                print("Candidate Found: ", candidate)

                # Update the candidate's field
                candidate.hr_round = "Scheduled"

                # Save the updated candidate
                candidate.save()

                print("Candidate Updated ", candidate)

            except candidate_master.DoesNotExist:
                print("Candidate Not Found")
        else:
            print("Not Updated")


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


# # Function to generate offer letter of the candidate....It will be called on generate offer letter button in scheduked interview.html.
# def generate_offer_letter(request,id):
#     get_id = id            # get the row id from generate offer letter button.
#     # query to get the data by Id
#
#     if request.method == 'GET'and get_id:
#         data = scheduled_interview.objects.filter(id=get_id).values()
#         context = {
#             'data': data
#         }
#         return render(request,'HR/generate_offer_letter.html',context)
#
#     elif request.method == 'POST' and get_id:
#         # Date Time section
#         d = date.today().strftime('%d ')
#         test_num = date.today().strftime('%m')
#         mnt = int(test_num)
#         m = calendar.month_name[mnt]
#         y = date.today().strftime(' %Y')
#
#         # input Section (This information)
#         name = request.POST.get("name")
#         designation = request.POST.get("designation")
#         position = request.POST.get("position")
#         joining_date = request.POST.get("joining_date")
#         package = request.POST.get("package")
#         in_words = request.POST.get("in_words")
#         location = request.POST.get("location")
#
#         print('Form data=',name,designation,position,joining_date,package,location)
#
#
#         # shows Replacements to be done on the documents.
#         change = {
#                   'name': name,
#                   'designation': designation,
#                   'position': position,
#                   'package': package,
#                   'joining_date': joining_date,
#                   'location': location,
#                    'in_words': in_words,
#                   }
#
#         # path to document
#         tpl = DocxTemplate('Offer_Nagpur.docx.')
#
#         # Replace
#         tpl.render(change)
#
#         # save the document
#         docName = name + "_Offer_Letter.doc"
#         tpl.save(docName)
#
#         # doc = aw.Document(docName)
#         # doc.save(name+".pdf")
#         # doc.save('Offer_Letter'+name+'_'+designation+'.docx')
#         # Converting it to PDF
#         #convert(docName, "pdf")
#
#         print("offer letter generated ")
#         return redirect(scheduled_interviews)

# Function to generate offer letter of the candidate....It will be called on generate offer letter button in scheduked interview.html.
def generate_offer_letter(request,id):
    id = id           # get the row id from generate offer letter button.
    print(id)
    # query to get the data by Id
    data = scheduled_interview.objects.get(id=id)
    email = data.email
    print(email)
    try:
        entry = offer_letter_detail.objects.get(email=email)
        entry_id = entry.id
        entry_data = offer_letter_detail.objects.get(id=entry_id)
        name = entry_data.name
        designation = entry_data.designation
        joining_date = entry_data.joining_date
        package = entry_data.package
        package_in_words = entry_data.package_in_words
        location = entry_data.location
        basic_da = entry_data.basic_da
        flexible_allowance = entry_data.flexible_allowance
        esic = entry_data.esic
        pt = entry_data.pt
        comp_esic_contribution = entry_data.comp_esic_contribution
        emp_code = entry_data.emp_code

        print(name)
        print(designation)
        print(joining_date)
        print(package)
        print(package_in_words)
        print(location)
        print(basic_da)
        print(flexible_allowance)
        print(esic)
        print(pt)
        print(comp_esic_contribution)
        print("Entry found with same email address")

        # Date Time section
        d = date.today().strftime('%d/%m/%Y')
        D = date.today().strftime('%d')
        mnt = int(date.today().strftime('%m'))
        m = calendar.month_name[mnt]
        y = date.today().strftime('%Y')
        date2 = f"{d}"
        date1 = f"{m} {D} {y}"

        name1 = name
        designation1 =designation
        total_monthly_gross = basic_da + flexible_allowance
        total_deduction = esic + pt
        monthly_net_pay = total_monthly_gross - total_deduction
        total_com_contribution = comp_esic_contribution
        total_ctc = total_monthly_gross + total_com_contribution

        # For Annual
        a_basic = basic_da * 12
        a_flexible_allowance = flexible_allowance * 12
        a_total_monthly_gross = total_monthly_gross * 12
        a_esic = esic * 12
        a_pt = pt * 12
        a_total_deduction = total_deduction * 12
        a_monthly_net_pay = monthly_net_pay * 12
        a_comp_esic_contribution = comp_esic_contribution * 12
        a_total_com_contribution = total_com_contribution * 12
        a_total_ctc = total_ctc * 12

        change = {'date': date1,
                  'name': name,
                  'designation': designation,
                  'package': package,
                  'in_words': package_in_words,
                  'name1': name1,
                  'code': emp_code,
                  'd1': designation1,
                  'joining_date': date2,
                  'location': location,
                  'b': basic_da,
                  'a_b': a_basic,
                  'fa': flexible_allowance,
                  'a_fa': a_flexible_allowance,
                  'tmg': total_monthly_gross,
                  'a_tmg': a_total_monthly_gross,
                  'e': esic,
                  'a_e': a_esic,
                  'pt': pt,
                  'a_pt': a_pt,
                  'td': total_deduction,
                  'a_td': a_total_deduction,
                  'mnp': monthly_net_pay,
                  'a_mnp': a_monthly_net_pay,
                  'cec': comp_esic_contribution,
                  'a_cec': a_comp_esic_contribution,
                  'tcc': total_com_contribution,
                  'a_tcc': a_total_com_contribution,
                  'tctc': total_ctc,
                  'a_tctc': a_total_ctc,

                  }

        # path to document
        tpl = DocxTemplate('offer_letter.docx')

        # Replace
        tpl.render(change)

        # save the document
        docName = name + "_Offer_Letter.doc"
        tpl.save(docName)
        print("Offer letter generated")
        os.startfile(docName)

        return redirect(scheduled_interviews)

    except offer_letter_detail.DoesNotExist:
        return HttpResponse('Offer letter not generated')


def generate_appointment_letter(request,id):
    id = id           # get the row id from generate offer letter button.
    print(id)
    # query to get the data by Id
    data = scheduled_interview.objects.get(id=id)
    email = data.email
    print(email)
    try:
        entry = offer_letter_detail.objects.get(email=email)
        entry_id = entry.id
        entry_data = offer_letter_detail.objects.get(id=entry_id)
        name = entry_data.name
        father_name = entry_data.father_name
        permanent_address = entry_data.permanent_address
        emp_code = entry_data.emp_code
        designation = entry_data.designation
        joining_date = entry_data.joining_date
        package = entry_data.package
        package_in_words = entry_data.package_in_words
        location = entry_data.location
        basic_da = entry_data.basic_da
        flexible_allowance = entry_data.flexible_allowance
        esic = entry_data.esic
        pt = entry_data.pt
        comp_esic_contribution = entry_data.comp_esic_contribution


       #Duplication of data and addition

        name1 = name
        name2 = name
        name3 = name
        code= emp_code
        designation1 = designation
        designation2 = designation
        designation3 = designation
        father_name1 = father_name
        address1 = permanent_address
        location1 = location
        total_monthly_gross = basic_da + flexible_allowance
        total_deduction = esic + pt
        monthly_net_pay = total_monthly_gross - total_deduction
        total_com_contribution = comp_esic_contribution
        total_ctc = total_monthly_gross + total_com_contribution


        # print(name)
        # print(designation)
        # print(joining_date)
        # print(package)
        print(package_in_words)
        # print(location)
        # print(basic_da)
        # print(flexible_allowance)
        # print(esic)
        # print(pt)
        # print(comp_esic_contribution)
        # print("Entry found with same email address")

        # Date Time section
        d = date.today().strftime('%d/%m/%Y')
        D = date.today().strftime('%d')
        mnt = int(date.today().strftime('%m'))
        m = calendar.month_name[mnt]
        y = date.today().strftime('%Y')
        date2 = f"{d}"
        date1 = f"{m} {D} {y}"
        date3 = date1
        date4 = date1
        date5 = date1

        # For Annual
        a_basic = basic_da * 12
        a_flexible_allowance = flexible_allowance * 12
        a_total_monthly_gross = total_monthly_gross * 12
        a_esic = esic * 12
        a_pt = pt * 12
        a_total_deduction = total_deduction * 12
        a_monthly_net_pay = monthly_net_pay * 12
        a_comp_esic_contribution = comp_esic_contribution * 12
        a_total_com_contribution = total_com_contribution * 12
        a_total_ctc = total_ctc * 12

        change = {'date1': date1,
                  'name': name,
                  'emp_code': emp_code,
                  'father_name' :father_name,
                  'address' : permanent_address,
                  'name1': name1,
                  'designation': designation,
                  'date3': date3,
                  'package': package,
                  'in_words': package_in_words,
                  'location': location,
                  'name2': name2,
                  'code': code,
                  'designation1': designation1,
                  'date4': date4,
                  'location1': location1,
                  'b': basic_da,
                  'a_b': a_basic,
                  'fa': flexible_allowance,
                  'a_fa': a_flexible_allowance,
                  'tmg': total_monthly_gross,
                  'a_tmg': a_total_monthly_gross,
                  'e': esic,
                  'a_e': a_esic,
                  'pt': pt,
                  'a_pt': a_pt,
                  'td': total_deduction,
                  'a_td': a_total_deduction,
                  'mnp': monthly_net_pay,
                  'a_mnp': a_monthly_net_pay,
                  'cec': comp_esic_contribution,
                  'a_cec': a_comp_esic_contribution,
                  'tcc': total_com_contribution,
                  'a_tcc': a_total_com_contribution,
                  'tctc': total_ctc,
                  'a_tctc': a_total_ctc,
                  'name3': name3,
                  'father_name1':father_name1,
                  'address1' : address1,
                  'date5':date5,
                  'designation2' : designation2,
                  'designation3' : designation3,

                  }

        # path to document
        tpl = DocxTemplate('appointment_letter.docx')

        # Replace
        tpl.render(change)

        # save the document
        docName = name + "_Appointment_Letter.doc"
        tpl.save(docName)
        print("Offer letter generated")
        os.startfile(docName)
        return redirect(scheduled_interviews)

    except offer_letter_detail.DoesNotExist:
        return redirect(scheduled_interviews)



def send_offer_mail(request,id):
    print("send offer mail function called ")
    get_id=id

    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        father_name = request.POST['father_name']
        permanent_address = request.POST['permanent_address']
        designation = request.POST['designation']
        joining_date = request.POST['joining_date']
        location = request.POST['location']
        basic_da = request.POST['basic']
        flexible_allowance = request.POST['flexible_allowance']
        esic = request.POST['esic']
        pt = request.POST['pt']
        package = request.POST['package']
        package_in_words = request.POST['package_in_words']
        emp_code = request.POST['emp_code']
        comp_esic_contribution = request.POST['comp_esic_contribution']
        service_level_agreement = request.POST['service_level_agreement']
        data = offer_letter_detail(name=name,email=email,designation=designation,joining_date=joining_date,location=location,basic_da=basic_da,
                                   flexible_allowance=flexible_allowance,father_name=father_name,permanent_address=permanent_address,
                                   esic=esic,pt=pt,comp_esic_contribution=comp_esic_contribution,
                                   service_level_agreement=service_level_agreement,package=package,package_in_words=package_in_words,emp_code=emp_code)

        data.save()


        date_obj = datetime.strptime(joining_date, '%Y-%m-%d')
        new_format = date_obj.strftime('%d-%m-%Y')
        print(new_format)


        print("Data saved")
        if email:
            print("Sending the offer mail ")
            subject, from_email, to = 'Offer Letter', 'python@iitms.co.in', 'hrmastersoft72@gmail.com'
            text_content = 'This is an important message.'
            html_content = f'Dear {name},<br><br>Greetings from Team MasterSoft !!<br><br>Congratulations and welcome to team MasterSoft!<br><br>With reference to your application and subsequent interview, We are pleased to inform you on your selection as {designation} at MasterSoft ERP Solutions Pvt Ltd.!<br><br>We are India’s leading education ERP provider with over 24 years of domain experience and we are excited to welcome you in our MasterSoft Family! <br><br>We are growing exponentially in India and globally in regions like the UAE, Middle East, Africa,Europe, US & UK.<br><br>We strongly believe that your skills and expertise will contribute to our companys growth to reach great heights!<br><br>We request you to join us on {new_format} and your Work Location will be {location}.<br><br> As discussed and agreed by you, the Service Level Agreement will be for {service_level_agreement}.<br><br>You are requested to upload the scanned copies of the documents before joining on the link http://localhost:8000/upload/ <br><br><u><b>Your appointment in the company is subject to a clear profile according to the Police Verification and only if you are medically fit.</u></b><br><br>We will look forward to your confirmation on the same within 24 hours and will provide you with the confirmed offer on the date of joining.<br><br>In case of any change or delay in the date of joining, must be informed in writing via mail and approved by us.<br><br>If in case you fail to join us on the agreed and confirmed date, the offer will stand revoked and cancelled automatically without any further clarification and communication.<br><br><b>Once again, congratulations and we look forward to welcoming you to Team MasterSoft!</b><br><br>If you have any questions or need additional information, please contact us.<br><br> Regards<br>HR Mastersoft'
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            print("Offer letter mail send")
            return redirect(scheduled_interviews)
        else:
            pass

    else:
        data = scheduled_interview.objects.filter(id=get_id).values()
        context = {
            'data': data
        }
        return render(request,'HR/offer_mail.html',context)

    return render(request,'HR/offer_mail.html')


# The function to view the resume of the candidate
from django.http import FileResponse


# function to view resume for applied candidate
def get_pdf2(request, id):
    get_id = id
    file_object = candidate_master.objects.get(id=get_id)
    response = FileResponse(file_object.resume)
    return response

#Function to view the candidate resume on applied candidate page
def get_pdf3(request, id):
    get_id = id
    file_object = candidate_application.objects.get(id=get_id)
    response = FileResponse(file_object.resume)
    return response

#Functions to view documents in canidate masters table
def get_pancard(request, id):
    get_id = id
    file_object = candidate_master.objects.get(id=get_id)
    response = FileResponse(file_object.pancard)
    return response

def get_address_proof(request, id):
    get_id = id
    file_object = candidate_master.objects.get(id=get_id)
    response = FileResponse(file_object.address_proof)
    return response

def get_photo_identity_proof(request, id):
    get_id = id
    file_object = candidate_master.objects.get(id=get_id)
    response = FileResponse(file_object.photo_identity_proof)
    return response


def get_ssc_certificate(request, id):
    get_id = id
    file_object = candidate_master.objects.get(id=get_id)
    response = FileResponse(file_object.ssc_certificate)
    return response

def get_hsc_certificate(request, id):
    get_id = id
    file_object = candidate_master.objects.get(id=get_id)
    response = FileResponse(file_object.hsc_certificate)
    return response

def get_diploma_certificate(request, id):
    get_id = id
    file_object = candidate_master.objects.get(id=get_id)
    response = FileResponse(file_object.diploma_certificate)
    return response

def get_degree_certificate(request, id):
    get_id = id
    file_object = candidate_master.objects.get(id=get_id)
    response = FileResponse(file_object.degree_certificate)
    return response

def get_pg_certificate(request, id):
    get_id = id
    file_object = candidate_master.objects.get(id=get_id)
    response = FileResponse(file_object.pg_certificate)
    return response

def get_college_tc(request, id):
    get_id = id
    file_object = candidate_master.objects.get(id=get_id)
    response = FileResponse(file_object.college_tc)
    return response

def get_passport_size_photo(request, id):
    get_id = id
    file_object = candidate_master.objects.get(id=get_id)
    response = FileResponse(file_object.passport_size_photo)
    return response

def get_bank_passbook(request, id):
    get_id = id
    file_object = candidate_master.objects.get(id=get_id)
    response = FileResponse(file_object.bank_passbook)
    return response

def get_internship_certificate(request, id):
    get_id = id
    file_object = candidate_master.objects.get(id=get_id)
    response = FileResponse(file_object.internship_certificate)
    return response

def get_experience_certificate(request, id):
    get_id = id
    file_object = candidate_master.objects.get(id=get_id)
    response = FileResponse(file_object.experience_certificate)
    return response

def get_last_salary_slip(request, id):
    get_id = id
    file_object = candidate_master.objects.get(id=get_id)
    response = FileResponse(file_object.last_salary_slip)
    return response

def get_form_16(request, id):
    get_id = id
    file_object = candidate_master.objects.get(id=get_id)
    response = FileResponse(file_object.form_16)
    return response

def get_passport(request, id):
    get_id = id
    file_object = candidate_master.objects.get(id=get_id)
    response = FileResponse(file_object.form_16)
    return response

def get_covid_vaccination_certificate(request, id):
    get_id = id
    file_object = candidate_master.objects.get(id=get_id)
    response = FileResponse(file_object.covid_vaccination_certificate)
    return response

def get_medical_certificate(request, id):
    get_id = id
    file_object = candidate_master.objects.get(id=get_id)
    response = FileResponse(file_object.covid_vaccination_certificate)
    return response

def get_police_verification_document(request, id):
    get_id = id
    file_object = candidate_master.objects.get(id=get_id)
    response = FileResponse(file_object.police_verification_document)
    return response
#______________________________________________________________________________________________________________________


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


def remove_scheduled_interview(request,id):
    if id is not None:
        obj = scheduled_interview.objects.get(id=id)
        obj.delete()
        return redirect(scheduled_interviews)
    else:
        pass




# #To remove the entry from the table Interview Scheduled Table for interview this function will be called on remove button
# def remove_scheduled_interview(request,id):
#     if id is not None:
#         obj = scheduled_interview.objects.get(id=id)
#         obj.delete()
#         return redirect('')
#     else:
#         pass

@csrf_exempt
def update_applied_candidate_status(request,id):
    print('inside func')
    id = id
    print(id)

    if request.method == 'POST':
        status = request.POST.get("status")
        print(status)
        rows_updated = candidate_application.objects.filter(id=id).update(status=status)
        applied_candidate = candidate_application.objects.get(id=id)
        candidate = candidate_application.objects.get(email=applied_candidate.email)
        email = applied_candidate.email
        print(email)

        try:
            candidate = candidate_master.objects.get(email=email)
            # If the code reaches here, it means a candidate with the given email exists
            # You can now access all the fields of the candidate using the `candidate` object
            candidate_id = candidate.id
            name = candidate.your_name
            email = candidate.email
            mobile_number = candidate.mobile_number
            father_name = candidate.father_name
            permanent_address = candidate.permanent_address
            resume = candidate.resume
            department = candidate.department
            position = candidate.position

            print('id= ',candidate_id)
            print("Entry found with same email address",name)
            if status:
                row_update_masters = candidate_master.objects.filter(id=candidate_id).update(status=status)
                print("Status updated in Candidate masters ")

                if status == 'Relevant':
                    #if relevant then neeed to add in scheduled table
                    print("Status of the candidate is Relevant")
                    data = scheduled_interview(name=name, email=email, contact_no=mobile_number,
                                               department=department, position=position,father_name=father_name,permanent_address=permanent_address
                                               )

                    data.save()
                    print("Data saved in scheduled interview table ")

                    #Code to remove cnadidate entry from applied candidate status
                    #candidate_application.objects.filter(id=id).delete()
                    print("Candidate removed form candidate application table")
                    return redirect(show_applicants)

                elif status == 'Irrelevant':
                    # Code to remove cnadidate entry from applied candidate status
                    candidate_application.objects.filter(id=id).delete()
                    print("Candidate removed form candidate application table")
                    return redirect(show_applicants)
                elif status == 'Position on Hold':
                    # Code to remove cnadidate entry from applied candidate status
                    candidate_application.objects.filter(id=id).delete()
                    print("Candidate removed form candidate application table")
                    return redirect(show_applicants)
                elif status == 'Position Closed':
                    # Code to remove cnadidate entry from applied candidate status
                    candidate_application.objects.filter(id=id).delete()
                    print("Candidate removed form candidate application table")
                    return redirect(show_applicants)
                else:
                    print("Inside the else part ")

            else:
                print("Status not found")
            # ... and so on for other fields
        except candidate_master.DoesNotExist:
            # If the code reaches here, it means no candidate with the given email exists
            print("Entry not found")
        return render(request, 'HR/applicant_data.html')


def update_status(request,id):
    id=id
    if request.method == 'POST':
        print("Inside update status",id)
        status = request.POST.get("status")
        print(status)

        schedule_candidate = scheduled_interview.objects.get(id=id)
        scheduled_interview.objects.filter(id=id).update(status=status)     #To update status in scheduled Interview table
        print("Status updated in scheduled interview table")
        print(schedule_candidate)
        candidate = scheduled_interview.objects.get(email=schedule_candidate.email)
        email = schedule_candidate.email
        print(email)

        try:
            candidate = candidate_master.objects.get(email=email)
            candidate_id = candidate.id
            name = candidate.your_name
            print("Entry found with same email address", name)
            if status:
                row_update_masters = candidate_master.objects.filter(id=candidate_id).update(status=status)
                print("Status of candidate updated in Candidate masters ")

                if status == 'Not Responding':
                    # Code to remove cnadidate entry from applied candidate status
                    #scheduled_interview.objects.filter(id=id).delete()
                    print("Candidate removed form candidate application table")
                elif status == 'Not Interested':
                    # Code to remove cnadidate entry from applied candidate status
                    #scheduled_interview.objects.filter(id=id).delete()
                    print("Candidate removed form candidate application table")
                elif status == 'Interview 1- Reject':
                    # Code to remove cnadidate entry from applied candidate status
                    #scheduled_interview.objects.filter(id=id).delete()
                    print("Candidate removed form candidate application table")
                elif status == 'Interview 2- Reject':
                    # Code to remove cnadidate entry from applied candidate status
                    #scheduled_interview.objects.filter(id=id).delete()
                    print("Candidate removed form candidate application table")
                elif status == 'Interview 3- Reject':
                    # Code to remove cnadidate entry from applied candidate status
                    #scheduled_interview.objects.filter(id=id).delete()
                    print("Candidate removed form candidate application table")
                elif status == 'Additional Round - Reject':
                    # Code to remove cnadidate entry from applied candidate status
                    #scheduled_interview.objects.filter(id=id).delete()
                    print("Candidate removed form candidate application table")
                elif status == 'Machine Test - Reject':
                    # Code to remove cnadidate entry from applied candidate status
                    #scheduled_interview.objects.filter(id=id).delete()
                    print("Candidate removed form candidate application table")
                elif status == 'HR Round - Reject':
                    # Code to remove cnadidate entry from applied candidate status
                    #scheduled_interview.objects.filter(id=id).delete()
                    print("Candidate removed form candidate application table")
                elif status == 'Candidature on Hold':
                    # Code to remove cnadidate entry from applied candidate status
                    #scheduled_interview.objects.filter(id=id).delete()
                    print("Candidate removed form candidate application table")
                elif status == 'Position on Hold':
                    # Code to remove cnadidate entry from applied candidate status
                    #scheduled_interview.objects.filter(id=id).delete()
                    print("Candidate removed form candidate application table")
                elif status == 'Position Closed':
                    # Code to remove cnadidate entry from applied candidate status
                    #scheduled_interview.objects.filter(id=id).delete()
                    print("Candidate removed form candidate application table")
                elif status == 'Offer Revoked':
                    # Code to remove cnadidate entry from applied candidate status
                    #scheduled_interview.objects.filter(id=id).delete()
                    print("Candidate removed form candidate application table")
                elif status == 'Ditched':
                    # Code to remove cnadidate entry from applied candidate status
                    #scheduled_interview.objects.filter(id=id).delete()
                    print("Candidate removed form candidate application table")
                elif status == 'Got Another Offer':
                    # Code to remove cnadidate entry from applied candidate status

                    #scheduled_interview.objects.filter(id=id).delete()
                    print("Candidate removed form candidate application table")

            else:
                print("Candidate status not found")
        except candidate_master.DoesNotExist:
            # If the code reaches here, it means no candidate with the given email exists
            print("Entry not found")

        return redirect(scheduled_interviews)
    return HttpResponse('get method called')


def feedback_page(request,id=None):
    print("Inside feedback function")
    id = id
    if id is not None:
        db_data = scheduled_interview.objects.get(id=id)
        candidate_name = db_data.name
        designation = db_data.position
        department_name = db_data.department
        print(db_data.email)
        interviewer_mail = db_data.interviewer_mail
        interviewer_name = db_data.interviewer
        print(interviewer_mail)

        Link = f'http://127.0.0.1:8000/feedback_update/{id}'          # Link for the feedback form
        #this will send mail to candidate
        subject, from_email, to = 'Feedback', 'python@iitms.co.in', interviewer_mail
        text_content = 'Feedback'
        html_content = f'Dear {interviewer_name},<br><br>In reference to the interview you have conducted of {candidate_name} for the {designation} position in the {department_name} Department, We request you to share your feedback on the given link.<br><br>Link"{Link}".<br><br>Please ensure the candidate details i.e Name, Department and Position on the webpage before submitting the feedback.<br><br>Thanks and regards,<br><br>HR Department<br>Mastersoft ERP Solutions Pvt. Ltd. '
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        print("Sending the mail to the interviewer")
        msg.send()
        print("Main Send to the Interviewer")
        return redirect(scheduled_interviews)

    return render(request,"HR/feedback.html")

# Interviewer will get the feedback form link and will submit the form then this fucntion will get called
def feedback_update(request,id):
    # Functuion that will update the Feedback into scheduled interview table
    print("Update Function called")
    id =id
    if request.method == 'POST':
        if id is not None:
            # get the data from the feedback form
            print("Post method called for id",id)
            name = request.POST['name']
            email = request.POST['email']
            department = request.POST['department']
            designation = request.POST['position']
            feedback_interview1 = request.POST['feedback_interview1']
            feedback_interview2 = request.POST['feedback_interview2']
            feedback_interview3 = request.POST['feedback_interview3']
            additional_round = request.POST['additional_round']
            machine_test = request.POST['machine_test']
            HR_round = request.POST['HR_round']

            print(name,email,designation,department,feedback_interview3,feedback_interview2,feedback_interview1,additional_round,machine_test,HR_round)

            data = scheduled_interview.objects.filter(id=id).update(feedback_interview1=feedback_interview1,feedback_interview2=feedback_interview2,
                                                                              feedback_interview3=feedback_interview3,additional_round=additional_round,machine_test=machine_test,
                                                                              HR_round=HR_round
                                                                              )
            print(type(data))
            print(data)

            print("feedback data updated in scheduled table for candidate" ,name)

            return render(request,'HR/feedback.html')

        else:
            print("id is None")
    else:
        data = scheduled_interview.objects.get(id=id)
        name = data.name
        email = data.email
        department = data.department
        designation = data.position
        print(name,email,department,designation)

        return render(request,'HR/feedback.html',{'name': name,'email': email,'department': department,'designation': designation})


def feedback_view(request,id):
    #Function to give the view of the candidate
    id=id

    data = scheduled_interview.objects.get(id=id)
    name = data.name
    email = data.email
    department = data.department
    designation = data.position
    feedback_interview1 = data.feedback_interview1
    feedback_interview2 = data.feedback_interview2
    feedback_interview3 = data.feedback_interview3
    additional_round = data.additional_round
    machine_test = data.machine_test
    HR_round = data.HR_round

    return render(request,'HR/feedback_view.html',{'name': name,'email': email,'department': department,'designation': designation,
                                                  'feedback_interview1': feedback_interview1,'feedback_interview2': feedback_interview2,'feedback_interview3': feedback_interview3,
                                                    'additional_round': additional_round,'machine_test': machine_test,'HR_round': HR_round
                                                  })











