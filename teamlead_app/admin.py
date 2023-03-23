from django.contrib import admin
from .models import requirement_raised,offer_letter_detail,candidate_master,upload_document,candidate_application,total_interviewer_bank,test_model,recruitment_master,optional_interviewer_bank,scheduled_interview
# Register your models here.

admin.site.register(recruitment_master)
admin.site.register(upload_document)
admin.site.register(candidate_master)
admin.site.register(candidate_application)
admin.site.register(scheduled_interview)
admin.site.register(requirement_raised)
admin.site.register(optional_interviewer_bank)
admin.site.register(test_model)
admin.site.register(total_interviewer_bank)
admin.site.register(offer_letter_detail)

