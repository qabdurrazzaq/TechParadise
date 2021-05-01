from .forms import CompanyLoginForm, CompanyRegistrationForm
from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.shortcuts import render, HttpResponseRedirect, Http404, HttpResponse
from django.urls import reverse
# Create your views here.

def company_login_view(request):
    request.session['sidebar_view'] = 1
    # if not request.user.is_authenticated:
    form = CompanyLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data['companyname']
        password = form.cleaned_data['companypassword']
        user = authenticate(username=username,password=password)
        if user.first_name == 'company' or user.is_superuser: 
            login(request,user,'django.contrib.auth.backends.ModelBackend')
            messages.success(request,'Successfully Logged In',extra_tags='safe')
            return HttpResponseRedirect(reverse('company',args=[request.user]))
        else:
            messages.error(request,'Incorrect Credentials')
            return HttpResponseRedirect(reverse('company_login'))
    context = {
        "form":form,
        'login':True,
    }
    return render(request, "company/form.html", context)
    # else:
    #     messages.warning(request,'Already Logged In')
    #     return HttpResponseRedirect(reverse('company',args=[request.user]))

def company_logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return HttpResponseRedirect(reverse('homepage'))
    else:
        return HttpResponseRedirect(reverse('company_login'))

def company_registration_view(request):
    company_form = CompanyRegistrationForm(request.POST or None)
    if company_form.is_valid():
        new_user = company_form.save(commit=False)
        new_user.first_name = 'company'
        new_user.save()
        messages.success(request, "Successfully Registered Company Account. Confirm your mail first.")
        return HttpResponseRedirect(reverse('company_register'))

    context = {
        "form":company_form,
    }
    return render(request, "company/form.html", context)

def company_view(request,user):
    context = {'user':user}
    return render(request,'company/company.html',context)