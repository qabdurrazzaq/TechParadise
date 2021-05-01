from django.contrib import admin
from .models import ConfirmEmail
# Register your models here.

class ConfirmEmailAdmin(admin.ModelAdmin):
    class Meta:
        model = ConfirmEmail

admin.site.register(ConfirmEmail,ConfirmEmailAdmin)

# class UserAdmin(admin.ModelAdmin):
#     class Meta:
#         list_display = ['__str__','is_superuser','is_applicant','is_company']
#         model = User

# admin.site.register(User,UserAdmin)