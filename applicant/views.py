from codeforces import api
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponseRedirect, Http404, HttpResponse
from django.urls import reverse
from github import Github
from .forms import ApplicantLoginForm, ApplicantRegistrationForm
from .models import ConfirmEmail, ApplicantDetail
import json
import os
import re
import requests

# Create your views here.

def applicant_login_view(request,backend='django.contrib.auth.backends.ModelBackend'):
    if not request.user.is_authenticated:
        form = ApplicantLoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username,password=password)
            login(request,user,backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request,'Successfully Logged In',extra_tags='safe')
            return HttpResponseRedirect(reverse('applicant',args=[request.user]))
        context = {
            "form":form,
            'login':True,
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
    request.session['sidebar_view'] = 1
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

def applicant_registration_view(request,backend='django.contrib.auth.backends.ModelBackend'):
    form = ApplicantRegistrationForm(request.POST or None)
    if form.is_valid():
        new_user = form.save(commit=False)
        new_user.save()
        messages.success(request, "Successfully Registered. Confirm your mail first.")
        return HttpResponseRedirect(reverse('applicant_register'))

    context = {
        "form":form,
    }
    return render(request, "applicant/form.html", context)

SHA1_RE = re.compile('^[a-f0-9]{40}$')

def email_activation_view(request,email_activation_key,backend='django.contrib.auth.backends.ModelBackend'):
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
            instance.save()
            login(request,instance.user,backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request,'Successfully Logged In',extra_tags='safe')
            return HttpResponseRedirect(reverse('applicant',args=[instance.user]))
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
    request.session['sidebar_view'] = 0
    context = {'user':user}
    return render(request,'applicant/applicant_details.html',context)

def applicant_google_login_view(request):
    return HttpResponseRedirect(reverse('applicant_google_login',args=['?process=login']))

def redirect_view(request):
    return HttpResponseRedirect(reverse('applicant',args=[request.user]))

def github_view(request,user):
    request.session['sidebar_view'] = 1
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
            messages.error(request,"Invalid Github Username")
            return HttpResponseRedirect(reverse('github',args=[user]))
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

def codeforces_view(request,user):
    request.session['sidebar_view'] = 1
    codeforces_api_key = settings.CODEFORCES_API_KEY
    codeforces_api_secret_key = settings.CODEFORCES_API_SECRET_KEY
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
        try:
            codeforces_user_info = api.call("user.info", key=codeforces_api_key, secret=codeforces_api_secret_key, handles=username)
            codeforces_rating = api.call("user.rating", key=codeforces_api_key, secret=codeforces_api_secret_key, handle=username)
            codeforces_rating.reverse()
            context = {
                "codeforces_user_info":codeforces_user_info[0],
                "codeforces_rating":codeforces_rating,
            }
        except:
            messages.error(request,'Invalid Codeforces UserName')
            return HttpResponseRedirect(reverse('codeforces',args=[user]))
    else:
        codeforces_user_info = None
        codeforces_rating = None
        context = {}
    
    return render(request,'applicant/codeforces.html',context)

def codechef_view(request,user):
    request.session['sidebar_view'] = 1
    username = request.GET.get('q')
    if username is not None:
        url = settings.X_RAPIDAPI_CODECHEF_URL + "/" + username
        headers = {
            'x-rapidapi-key': settings.X_RAPIDAPI_CODECHEF_KEY,
            'x-rapidapi-host': settings.X_RAPIDAPI_CODECHEF_HOST,
        }
        response = requests.request("GET", url, headers=headers)
        codechef = json.loads(response.text)
        if codechef['status'] == 'Failed':
            codechef = None
            messages.error(request,'Invalid CodeChef Username')
            return HttpResponseRedirect(reverse('codechef',args=[user]))
        else:
            context={'codechef':codechef}
    else:
        context = {}
    return render(request,'applicant/codechef.html',context)