from django.contrib import admin
from .models import ConfirmEmail, User
# Register your models here.

class ConfirmEmailAdmin(admin.ModelAdmin):
    class Meta:
        model = ConfirmEmail

admin.site.register(ConfirmEmail,ConfirmEmailAdmin)

admin.site.register(User)