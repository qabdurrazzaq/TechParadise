from django.contrib.auth import logout, login
from django.contrib import messages
from django.shortcuts import render, HttpResponseRedirect, Http404
from django.urls import reverse
from .models import ConfirmEmail
import re

# Create your views here.

def homepage_view(request):
    request.session['sidebar_view'] = 0
    context = {}
    return render(request, 'home/homepage.html',context)

def session_logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('homepage'))

SHA1_RE = re.compile('^[a-f0-9]{40}$')

def email_activation_view(request,email_activation_key,backend='django.contrib.auth.backends.ModelBackend'):
    if SHA1_RE.search(email_activation_key):
        try:
            instance = ConfirmEmail.objects.get(email_activation_key=email_activation_key)
        except:
            instance = None
        if instance is not None and not instance.confirmed:
            page_message = "Confirmation Successful"
            instance.confirmed = True
            instance.email_activation_key = "Confirmed"
            instance.save()
            login(request,instance.user,backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request,'Successfully Logged In',extra_tags='safe')
            return HttpResponseRedirect(reverse('applicant',args=[instance.user]))
        elif instance is not None and instance.confirmed:
            page_message = "Email Already Confirmed"
        else:
            page_message=''

        context = {"page_message":page_message}
        return render(request,"home/activation_status.html",context)
    else:
        raise Http404