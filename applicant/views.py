from codeforces import api
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponseRedirect, Http404, HttpResponse
from django.urls import reverse
from github import Github
from home.models import UserRole
from .forms import ApplicantLoginForm, ApplicantRegistrationForm
from .models import ApplicantDetail
import json
import requests

# Create your views here.

def applicant_login_view(request,backend='django.contrib.auth.backends.ModelBackend'):
    if request.user.is_authenticated:
        logout(request)
        return HttpResponseRedirect(reverse('applicant_login'))
    else:
        form = ApplicantLoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username,password=password)
            if user.is_applicant or user.is_superuser:
                login(request,user,backend='django.contrib.auth.backends.ModelBackend')
                messages.success(request,'Successfully Logged In')
                return HttpResponseRedirect(reverse('applicant',args=[request.user]))
            else:
                messages.error(request,'Invalid Username Or Password')
                return HttpResponseRedirect(reverse('applicant_login'))
        context = {
            'form':form,
            'login':True,
        }
        return render(request,'applicant/form.html',context)

def applicant_view(request, user):
    if not request.user.is_authenticated:
        messages.error(request,'You are logged out or not authenticated')
        return HttpResponseRedirect(reverse('applicant_login'))
    elif request.user.is_applicant or request.user.is_superuser:
        if request.user.is_authenticated and str(user) == str(request.user):
            try:
                applicant_det = request.session['applicant_det']
            except Exception as e:
                print(e)
                applicant_det = None
            try:
                applicant_details_user = ApplicantDetail.objects.get_or_create(user=request.user)
            except Exception as e:
                print(e)
                HttpResponseRedirect(reverse('applicant_login'))
            try:
                applicant_details = ApplicantDetail.objects.get(user=request.user)
            except Exception as e:
                print(e)
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
                except Exception as e:
                    print(e)
                    applicant_details.github_username = None
                if applicant_details.github_username is not None:
                    access_token = settings.GIT_API_TOKEN
                    g = Github(access_token)
                    try:
                        git_user = g.get_user(applicant_details.github_username)
                    except Exception as e:
                        print(e)
                        git_user = None
                        messages.error(request,"Invalid Github Username")
                        return HttpResponseRedirect(reverse('applicant_details',args=[request.user]))
                applicant_details.save()
                context = {'applicant_details':applicant_details}
                request.session['applicant_det'] = 0
            else:
                context = {'applicant_details':applicant_details,'user':user}
            return render(request,"applicant/applicant.html",context)
        elif str(user) != str(request.user):
            messages.error(request,'This username account has been logged out. Try logging again')
            logout(request)
            return HttpResponseRedirect(reverse('applicant_login'))
        else:
            messages.error(request,'Invalid Username or Password')
            if request.user.is_authenticated:
                logout(request)
            return HttpResponseRedirect(reverse('applicant_login'))
    else:
        request.user.is_applicant = True
        return HttpResponseRedirect(reverse('applicant_login'))

def applicant_registration_view(request):
    if request.user.is_authenticated:
        logout(request)
        return HttpResponseRedirect(reverse('applicant_register'))
    else:
        print('applicant_register')
        applicant_form = ApplicantRegistrationForm(request.POST or None)
        if applicant_form.is_valid():
            new_user = applicant_form.save(commit=False)
            new_user.is_applicant = True
            new_user.save()
            messages.success(request, "Successfully Registered. Confirm your mail first.")
            return HttpResponseRedirect(reverse('applicant_register'))
        context = {
            "form":applicant_form,
        }
        return render(request, "applicant/form.html", context)

def set_applicant_user_role_view(request):
    role = UserRole()
    role.user_role = 'applicant'
    role.save()
    return HttpResponseRedirect(reverse('applicant_google_login'))

def applicant_google_login_view(request):
    return HttpResponseRedirect(reverse('applicant_google_login',args=['/?process=login']))

def applicant_details_view(request,user):
    if request.user.is_authenticated:
        request.session['applicant_det'] = 1
        context = {'user':user}
        return render(request,'applicant/applicant_details.html',context)
    else:
        messages.error(request,'You are logged out or not authenticated')
        return HttpResponseRedirect(reverse('applicant_login'))

def github_view(request,user):
    access_token = settings.GIT_API_TOKEN
    try:
        username = request.GET.get('q')
        if username is None:
            try:
                applicant_details = ApplicantDetail.objects.get(user=request.user)
            except Exception as e:
                print(e)
                applicant_details = None
            if applicant_details is not None:
                if applicant_details.github_username is not None:
                    username = applicant_details.github_username
                else:
                    username = None
            else:
                username = None
    except Exception as e:
        print(e)
        username = None
    if username is not None:
        g = Github(access_token)
        try:
            git_user = g.get_user(username)
        except Exception as e:
            print(e)
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
    codeforces_api_key = settings.CODEFORCES_API_KEY
    codeforces_api_secret_key = settings.CODEFORCES_API_SECRET_KEY
    try:
        username = request.GET.get('q')
    except Exception as e:
        print(e)
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
        except Exception as e:
            print(e)
            messages.error(request,'Invalid Codeforces UserName')
            return HttpResponseRedirect(reverse('codeforces',args=[user]))
    else:
        codeforces_user_info = None
        codeforces_rating = None
        context = {}
    
    return render(request,'applicant/codeforces.html',context)

def codechef_view(request,user):
    username = request.GET.get('q')
    if username is not None:
        url = settings.X_RAPIDAPI_CODECHEF_URL + "/" + username
        headers = {
            'x-rapidapi-key': settings.X_RAPIDAPI_CODECHEF_KEY,
            'x-rapidapi-host': settings.X_RAPIDAPI_CODECHEF_HOST,
        }
        response = requests.request("GET", url, headers=headers)
        codechef = json.loads(response.text)
        try:
            status = codechef['status']
        except Exception as e:
            print(e)
            status = None
        if not status:
            codechef = None
            messages.error(request,'Invalid CodeChef Username')
            return HttpResponseRedirect(reverse('codechef',args=[user]))
        else:
            context={'codechef':codechef}
    else:
        context = {}
    return render(request,'applicant/codechef.html',context)

def leetcode_view(request,user):
    username = request.GET.get('q')
    if username is not None:
        url = settings.LEETCODE_URL + "/" + username
        response = requests.request("GET", url)
        leetcode = json.loads(response.text)
        if leetcode['status'] == 'Failed':
            leetcode = None
            messages.error(request,'Invalid Leetcode Username')
            return HttpResponseRedirect(reverse('leetcode',args=[user]))
        else:
            context={
                'leetcode':leetcode,
                'username':username
            }
    else:
        context = {}
    return render(request,'applicant/leetcode.html',context)