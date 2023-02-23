"""hr_recruitment URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from teamlead_app import views

urlpatterns = [

    path('admin/', admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),  # Built in login, logout, and password management.
    path("logout/index/", views.index, name="index"),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path("login/home/",views.home, name='home'),
    #path("",views.home,name='home'),
    path("raise_requirement_form", views.raise_requirement_form, name='raise_requirement_form'),
    path("home/raise_requirement_form", views.raise_requirement_form, name='raise_requirement_form'),
    path("home/current_requirement", views.current_requirement, name='current_requirement'),
    path("",views.index,name='index'),


    #path("main/",views.main,name='main'),
    path("register/",views.register,name="register"),
    path('hr_view/',views.hr_view, name='hr_view'),
    path('hr_view/register/', views.register, name='register2'),
    path('hr_view/', views.hr_view, name='hr_view'),


# ----------------- Apply form link path ---------------------------
    path('apply/', views.Apply_form, name='apply'),
# ------------------- Ends here -------------------------

    path('upload/', views.document_upload_form, name='upload'),
    path('hr_view/showapplicants/', views.show_applicants, name='showapplicants1'),
    path('hr_view/showapplicants/<int:id>', views.show_applicants, name='showapplicants2'),
    path('hr_view/selected_applicants/', views.all_selected_candidate, name='selected_applicants1'),
    path('hr_view/selected_applicants/<int:id>', views.selected_candidate, name='selected_applicants2'),

    path('hr_view/scheduled_interview/', views.scheduled_interviews, name='scheduled_interviews'),
    path('hr_view/nextround_interview_scheduling/<int:id>', views.round_two_interview_scheduling, name='round_two_interview_scheduling'),
    path('hr_view/machine_test_interview_scheduling/<int:id>', views.round_three_machine_test_scheduling, name='round_three_machine_test_scheduling'),
    path('hr_view/HR_round_interview_scheduling/<int:id>', views.round_four_hr_round_scheduling, name='round_four_hr_round_scheduling'),
    path('hr_view/generate_offer_letter/<int:id>', views.generate_offer_letter, name='generate_offer_letter'),

    #path('/hr_view/selected_applicants/interview_schedule/', views.interview_schedule, name='interview_schedule'),
    #path('hr_view/showapplicants/', views.show_applicants, name='showapplicants1'),
    path('hr_view/schedule/<int:id>', views.interview_schedule, name='schedule'),

    path('hr_view/raise_requirement/', views.hr_raise_requirement, name='hr_raise_requirement'),
    #path('hr_view/all_requirement/', views.all_requirement, name='all_requirement'),
    path('hr_view/update_budget/', views.update_budget, name='update_budget'),
    path('get_pdf/<int:id>', views.get_pdf, name='get_pdf'),
    path('get_pdf2/<int:id>', views.get_pdf2, name='get_pdf2'),    #For resumes in applied candidate
    path('hr_view/candidate_master/', views.candidate_master_view, name='candidate_master_view'),
    path('hr_view/requirement_master/', views.recruitment_master_view, name='recruitment_master_view'),
    path('hr_view/selected_applicants/remove/<int:id>', views.remove_selected_candidate_interview, name='remove_selected_candidate_interview'),
    path('hr_view/scheduled_interview/remove/<int:id>', views.remove_scheduled_interview, name='remove_scheduled_interview'),

    # testing path local
    path('test/', views.test, name='test'),


]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# To make changes in a django admin panel
admin.site.site_header = "DB Dashboard"
admin.site.site_title = " Admin Portal"
admin.site.index_title = "Welcome to Recruitment Portal"
