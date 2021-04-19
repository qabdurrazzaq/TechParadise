"""TechParadise URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path, include
from applicant import views as applicantviews

urlpatterns = [

    # url for admin
    path('admin/', admin.site.urls),

    # url for applicant app
    path('applicant/accounts/login/',applicantviews.applicant_login_view,name='applicant_login'),
    path('applicant/accounts/logout/',applicantviews.applicant_logout_view,name='applicant_logout'),
    path('applicant/accounts/register/',applicantviews.applicant_registration_view,name='applicant_register'),
    re_path(r'^applicant/(?P<user>\w+)/$',applicantviews.applicant_view,name='applicant'),
    re_path(r'^applicant/(?P<user>\w+)/details',applicantviews.applicant_details_view,name='applicant_details'),
    path('redirect/',applicantviews.redirect_view,name='redirect'),
    path('accounts/', include('allauth.urls')),
    path('accounts/google/login/',applicantviews.applicant_google_login_view,name='applicant_google_login'),
    re_path(r'^applicant/activate/(?P<email_activation_key>\w+)/$', applicantviews.email_activation_view, name = 'email_activation_view'),
    re_path(r'^applicant/(?P<user>\w+)/github/$',applicantviews.github_view,name='github'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
