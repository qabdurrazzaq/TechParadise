from .forms import CompanyLoginForm, CompanyRegistrationForm
from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.shortcuts import render, HttpResponseRedirect, Http404, HttpResponse
from django.urls import reverse
from home.models import UserRole
from .models import CompanyDetail,Quarter
# Create your views here.

def company_login_view(request):
    if request.user.is_authenticated:
        logout(request)
        return HttpResponseRedirect(reverse('company_login'))
    else:
        form = CompanyLoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['companyname']
            password = form.cleaned_data['companypassword']
            user = authenticate(username=username,password=password)
            if user.is_company or user.is_superuser:
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
    return HttpResponseRedirect(reverse('company_google_login'))

def company_google_login_view(request):
    return HttpResponseRedirect(reverse('company_google_login',args=['/?process=login']))

def company_view(request,user):
    # if not request.user.is_authenticated:
    #     messages.error(request,'You are logged out or not authenticated')
    #     return HttpResponseRedirect(reverse('company_login'))
    # elif request.user.is_company and request.user.is_authenticated:
    #     context = {'user':user}
    #     return render(request,'company/company.html',context)
    # elif str(user) != str(request.user):
    #     messages.error(request,'This username account has been logged out or not registered. Try again')
    #     if request.user.is_authenticated:
    #         logout(request)
    #     return HttpResponseRedirect(reverse('company_login'))
    # else:
    #     messages.error(request,'Invalid Username or Password')
    #     if request.user.is_authenticated:
    #         logout(request)
    #     return HttpResponseRedirect(reverse('applicant_login'))
    if not request.user.is_authenticated:
        messages.error(request,'You are logged out or not authenticated')
        return HttpResponseRedirect(reverse('company_login'))
    elif request.user.is_company or request.user.is_superuser:
        if request.user.is_authenticated and str(user) == str(request.user):
            try:
                company_det = request.session['company_det']
            except Exception as e:
                print(e)
                company_det = None
            try:
                company_details_user = CompanyDetail.objects.get_or_create(user=request.user)
            except Exception as e:
                print(e)
                HttpResponseRedirect(reverse('company_login'))
            try:
                company_details = CompanyDetail.objects.get(user=request.user)
            except Exception as e:
                print(e)
                company_details = None
            try:
                company_quarter_details_user = Quarter.objects.get_or_create(user=request.user)
            except Exception as e:
                print(e)
                HttpResponseRedirect(reverse('company_login'))
            try:
                company_quarter_details = Quarter.objects.get(user=request.user)
            except Exception as e:
                print(e)
                company_quarter_details = None
            if company_det == 1:
                company_details.headquarter = request.POST.get('headquarter')
                company_details.achievements = request.POST.get('achievements')
                company_details.about = request.POST.get('about')
                company_details.save()
                company_quarter_details.subquarter = request.POST.get('subquarter')
                company_quarter_details.save()
                context = {
                    'company_details':company_details,
                    'company_quarter_details':company_quarter_details,
                }
                request.session['company_det'] = 0
            else:
                context = {'company_details':company_details,'user':user}
            return render(request,"company/company.html",context)
        elif str(user) != str(request.user):
            messages.error(request,'This username account has been logged out. Try logging again')
            logout(request)
            return HttpResponseRedirect(reverse('company_login'))
        else:
            messages.error(request,'Invalid Username or Password')
            if request.user.is_authenticated:
                logout(request)
            return HttpResponseRedirect(reverse('company_login'))
    else:
        request.user.is_company = True
        return HttpResponseRedirect(reverse('company_login'))

def company_details_view(request,user):
    if request.user.is_authenticated:
        request.session['company_det'] = 1
        context = {'user':user}
        return render(request,'company/company_details.html',context)
    else:
        messages.error(request,'You are logged out or not authenticated')
        return HttpResponseRedirect(reverse('company_login'))