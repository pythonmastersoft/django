from django.contrib import admin
from .models import candidate_application,total_interviewer_bank,test_model,document,recruitment_master,optional_interviewer_bank,candidate_master,scheduled_interview,selected_candidate_interview
# Register your models here.

admin.site.register(recruitment_master)
admin.site.register(candidate_master)
admin.site.register(candidate_application)
admin.site.register(scheduled_interview)
admin.site.register(selected_candidate_interview)
admin.site.register(document)
admin.site.register(optional_interviewer_bank)
admin.site.register(test_model)
admin.site.register(total_interviewer_bank)
