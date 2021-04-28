from django.contrib.auth import logout
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse

# Create your views here.

def homepage_view(request):
    request.session['sidebar_view'] = 0
    context = {}
    return render(request, 'home/homepage.html',context)

def session_logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('homepage'))