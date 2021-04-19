from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponseRedirect, Http404, HttpResponse
from django.urls import reverse
from github import Github
from .forms import ApplicantLoginForm, ApplicantRegistrationForm
from .models import ConfirmEmail, ApplicantDetail
import os
import re

# Create your views here.

def applicant_login_view(request):
    if not request.user.is_authenticated:
        # google_client_id = settings.GOOGLE_CLIENT_ID
        form = ApplicantLoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username,password=password)
            login(request,user)
            messages.success(request,'Successfully Logged In',extra_tags='safe')
            return HttpResponseRedirect(reverse('applicant',args=[request.user]))
        context = {
            "form":form,
            'login':True,
            # "google_client_id":google_client_id,
        }
        return render(request, "applicant/form.html", context)
    else:
        messages.warning(request,'Already Logged In')
        return HttpResponseRedirect(reverse('applicant',args=[request.user]))


def applicant_logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return HttpResponseRedirect(reverse('applicant_login'))
    else:
        return HttpResponseRedirect(reverse('applicant_login'))

# @login_required
def applicant_view(request, user):
    if request.user.is_authenticated and str(user) == str(request.user):
        try:
            applicant_det = request.session['applicant_det']
        except:
            applicant_det = None
            pass
        try:
            applicant_details_user = ApplicantDetail.objects.get_or_create(user=request.user)
        except:
            HttpResponseRedirect(reverse('applicant_login'))
        try:
            applicant_details = ApplicantDetail.objects.get(user=request.user)
        except:
            applicant_details = None
        if applicant_det == 1:
            applicant_details.first_name = request.POST.get('first_name')
            applicant_details.last_name = request.POST.get('last_name')
            applicant_details.qualification = request.POST.get('qualification')
            applicant_details.interest = request.POST.get('interest')
            applicant_details.achievements = request.POST.get('achievements')
            applicant_details.about = request.POST.get('about')
            try:
                applicant_details.github_username = request.POST.get('github_username')
            except:
                applicant_details.github_username = None
            if applicant_details.github_username is not None:
                access_token = settings.GIT_API_TOKEN
                g = Github(access_token)
                try:
                    git_user = g.get_user(applicant_details.github_username)
                except:
                    git_user = None
                    messages.error(request,"Invalid Github Username")
                    return HttpResponseRedirect(reverse('applicant_details',args=[request.user]))
            applicant_details.save()
            context = {'applicant_details':applicant_details}
            request.session['applicant_det'] = 0
        else:
            context = {'applicant_details':applicant_details,'user':user}
        return render(request,"applicant/applicant.html",context)
    elif not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('applicant_login'))
    elif str(user) != str(request.user):
        raise NameError('please enter username of currently logged in user')

def applicant_registration_view(request):
    google_client_id = settings.GOOGLE_CLIENT_ID
    form = ApplicantRegistrationForm(request.POST or None)
    if form.is_valid():
        new_user = form.save(commit=False)
        new_user.save()
        messages.success(request, "Successfully Registered. Confirm your mail first.")
        return HttpResponseRedirect(reverse('applicant_register'))

    context = {
        "form":form,
        "google_client_id":google_client_id,
    }
    return render(request, "applicant/form.html", context)

SHA1_RE = re.compile('^[a-f0-9]{40}$')

def email_activation_view(request,email_activation_key):
    if SHA1_RE.search(email_activation_key):
        try:
            instance = ConfirmEmail.objects.get(email_activation_key=email_activation_key)
        except:
            instance = None
            raise Http404
        if instance is not None and not instance.confirmed:
            page_message = "Confirmation Successful"
            instance.confirmed = True
            instance.email_activation_key = "Confirmed"
            login(request,instance.user)
            messages.success(request,'Successfully Logged In',extra_tags='safe')
            return HttpResponseRedirect(reverse('applicant'))
            instance.save()
        elif instance is not None and instance.confirmed:
            page_message = "Email Already Confirmed"
        else:
            page_message=""

        context = {"page_message":page_message}
        return render(request,"applicant/activation_status.html",context)
    else:
        raise Http404

def applicant_details_view(request,user):
    request.session['applicant_det'] = 1
    context = {'user':user}
    return render(request,'applicant/applicant_details.html',context)

def github_view(request,user):
    access_token = settings.GIT_API_TOKEN
    try:
        username = request.GET.get('q')
        if username is None:
            try:
                applicant_details = ApplicantDetail.objects.get(user=request.user)
            except:
                applicant_details = None
            if applicant_details is not None:
                if applicant_details.github_username is not None:
                    username = applicant_details.github_username
                else:
                    username = None
            else:
                username = None
    except:
        username = None
    if username is not None:
        g = Github(access_token)
        try:
            git_user = g.get_user(username)
        except:
            git_user = None
        if git_user is not None:
            repos = git_user.get_repos()
        else:
            repos=None
            pass
        context={
            'repos':repos,
            "git_user":git_user,
            "username":username,
        }
    else:
        context = {}
    return render(request,'applicant/github.html',context)

def applicant_google_login_view(request):
    return HttpResponseRedirect(reverse('applicant_google_login',args=['?process=login']))

def redirect_view(request):
    return HttpResponseRedirect(reverse('applicant',args=[request.user]))