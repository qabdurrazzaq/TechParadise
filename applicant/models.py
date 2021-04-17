from django.core.mail import send_mail
from django.conf import settings
from django.db import models
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
# Create your models here.

class ApplicantDetail(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=True,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=120,null=True,blank=True)
    last_name = models.CharField(max_length=120,null=True,blank=True)
    qualification = models.CharField(max_length=200,null=True,blank=True)
    achievements = models.CharField(max_length=200,null=True,blank=True)
    interest = models.CharField(max_length=200,null=True,blank=True)
    github_username = models.CharField(max_length=200,null=True,blank=True)
    about = models.TextField(max_length=250,null=True,blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.first_name)

class ConfirmEmail(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    email_activation_key = models.CharField(max_length=200)
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return "Email Confirmed is: " + str(self.confirmed)

    def activate_user_email(self):
        print("activation: %s" %(self.email_activation_key))
        email_activation_url = "http://localhost:8000%s" %(reverse("email_activation_view",args=[self.email_activation_key]))
        context = {
            "email_activation_key":self.email_activation_key,
            "email_activation_url":email_activation_url,
            "user":self.user.username,
        }
        subject = "Activate Your Email"
        message = render_to_string('applicant/email_activation_message.txt',context)
        self.email_user(subject,message,settings.DEFAULT_FROM_EMAIL)

    def email_user(self,subject,message,from_email=None,**kwargs):
        send_mail(subject,message,from_email,[self.user.email],kwargs)
