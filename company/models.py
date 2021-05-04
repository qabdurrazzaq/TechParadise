from django.conf import settings
from django.db import models
from django.utils import timezone
# Create your models here.

class CompanyDetail(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=True,on_delete=models.CASCADE)
    headquarter = models.CharField(max_length=120,null=True,blank=True)
    achievements = models.CharField(max_length=200,null=True,blank=True)
    about = models.TextField(max_length=250,null=True,blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.user)

class Quarter(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=True,on_delete=models.CASCADE)
    subquarter = models.CharField(max_length=120,null=True,blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.user)