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
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,'Successfully Logged Out')
        return HttpResponseRedirect(reverse('homepage'))
    else:
        messages.error(request,'Already Logged Out')
        return HttpResponseRedirect(reverse('homepage'))

SHA1_RE = re.compile('^[a-f0-9]{40}$')

def email_activation_view(request,email_activation_key,backend='django.contrib.auth.backends.ModelBackend'):
    if SHA1_RE.search(email_activation_key):
        print('home email activation view')
        try:
            instance = ConfirmEmail.objects.get(email_activation_key=email_activation_key)
        except Exception as e:
            e.printStackTrace()
            instance = None
        if instance is not None and not instance.confirmed:
            page_message = "Confirmation Successful"
            instance.confirmed = True
            instance.email_activation_key = "Confirmed"
            instance.save()
            login(request,instance.user,backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request,'Successfully Logged In',extra_tags='safe')
            if instance.user.is_applicant:
                return HttpResponseRedirect(reverse('applicant',args=[instance.user]))
            elif instance.user.is_company:
                return HttpResponseRedirect(reverse('company',args=[instance.user]))
            else:
                return HttpResponseRedirect(reverse('homepage'))
        elif instance is not None and instance.confirmed:
            page_message = "Email Already Confirmed"
        else:
            page_message=''

        context = {"page_message":page_message}
        return render(request,"home/activation_status.html",context)
    else:
        raise Http404

def redirect_view(request):
    print('redirect '+str(request.user))
    return HttpResponseRedirect(reverse('applicant',args=[request.user]))

def google_login_view(request):
    return HttpResponseRedirect(reverse('google_login',args=['/?process=login']))