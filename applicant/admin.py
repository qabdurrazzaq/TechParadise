from django.contrib import admin
from .models import ApplicantDetail

class ApplicantDetailAdmin(admin.ModelAdmin):
    class Meta:
        model = ApplicantDetail

admin.site.register(ApplicantDetail,ApplicantDetailAdmin)