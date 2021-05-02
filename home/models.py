from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.template.loader import render_to_string

# Create your models here.
class ConfirmEmail(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    email_activation_key = models.CharField(max_length=200)
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return "Email Confirmed is: " + str(self.confirmed)

    def activate_user_email(self):
        email_activation_url = "http://localhost:8000%s" %(reverse("email_activation",args=[self.email_activation_key]))
        context = {
            "email_activation_key":self.email_activation_key,
            "email_activation_url":email_activation_url,
            "user":self.user.username,
        }
        subject = "Activate Your Email"
        message = render_to_string('home/email_activation_message.txt',context)
        self.email_user(subject,message,settings.DEFAULT_FROM_EMAIL)

    def email_user(self,subject,message,from_email=None,**kwargs):
        send_mail(subject,message,from_email,[self.user.email],kwargs)

class User(AbstractUser):
    is_applicant = models.BooleanField(default=False)
    is_company = models.BooleanField(default=False)