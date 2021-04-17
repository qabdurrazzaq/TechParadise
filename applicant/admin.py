from django.contrib import admin
from .models import ConfirmEmail, ApplicantDetail
# Register your models here.
class ConfirmEmailAdmin(admin.ModelAdmin):
    class Meta:
        model = ConfirmEmail

admin.site.register(ConfirmEmail,ConfirmEmailAdmin)

class ApplicantDetailAdmin(admin.ModelAdmin):
    class Meta:
        model = ApplicantDetail

admin.site.register(ApplicantDetail,ApplicantDetailAdmin)