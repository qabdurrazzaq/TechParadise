from .forms import CompanyLoginForm, CompanyRegistrationForm
from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.shortcuts import render, HttpResponseRedirect, Http404, HttpResponse
from django.urls import reverse
from home.models import UserRole
# Create your views here.

def company_login_view(request):
    if request.user.is_authenticated:
        logout(request)
        return HttpResponseRedirect(reverse('company_login'))
    else:
        form = CompanyLoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username,password=password)
            if user.is_Company or user.is_superuser:
                login(request,user,backend='django.contrib.auth.backends.ModelBackend')
                messages.success(request,'Successfully Logged In')
                return HttpResponseRedirect(reverse('company',args=[request.user]))
            else:
                messages.error(request,'Invalid Username Or Password')
                return HttpResponseRedirect(reverse('company_login'))
        context = {
            'form':form,
            'login':True,
        }
        return render(request,'company/form.html',context)

def company_registration_view(request):
    if request.user.is_authenticated:
        logout(request)
        return HttpResponseRedirect(reverse('company_register'))
    else:
        company_form = CompanyRegistrationForm(request.POST or None)
        if company_form.is_valid():
            new_user = company_form.save(commit=False)
            new_user.is_company = True
            new_user.save()
            messages.success(request, "Successfully Registered Company Account. Confirm your mail first.")
            return HttpResponseRedirect(reverse('company_register'))

        context = {
            "form":company_form,
        }
        return render(request, "company/form.html", context)

def set_company_user_role_view(request):
    role = UserRole()
    role.user_role = 'company'
    role.save()
    return HttpResponseRedirect(reverse('applicant_google_login'))

def company_google_login_view(request):
    return HttpResponseRedirect(reverse('company_google_login',args=['/?process=login']))

def company_view(request,user):
    if not request.user.is_authenticated:
        messages.error(request,'You are logged out or not authenticated')
        return HttpResponseRedirect(reverse('company_login'))
    elif request.user.is_company and request.user.is_authenticated:
        context = {'user':user}
        return render(request,'company/company.html',context)
    elif str(user) != str(request.user):
        messages.error(request,'This username account has been logged out. Try logging again')
        if request.user.is_authenticated:
            logout(request)
        return HttpResponseRedirect(reverse('company_login'))
    else:
        messages.error(request,'Invalid Username or Password')
        if request.user.is_authenticated:
            logout(request)
        return HttpResponseRedirect(reverse('applicant_login'))