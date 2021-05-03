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
from company import views as companyviews
from home import views as homeviews

urlpatterns = [

    # url for admin
    path('admin/', admin.site.urls),

    # url for home app
    path('',homeviews.homepage_view,name='homepage'),
    path('accounts/logout',homeviews.session_logout_view,name='session_logout'),
    re_path(r'^accounts/activate/(?P<email_activation_key>\w+)/$', homeviews.email_activation_view, name = 'email_activation'),
    path('redirect/',homeviews.redirect_view,name='redirect'),
    path('accounts/', include('allauth.urls')),

    # url for applicant app
    path('applicant/accounts/login/',applicantviews.applicant_login_view,name='applicant_login'),
    path('applicant/accounts/register/',applicantviews.applicant_registration_view,name='applicant_register'),
    re_path(r'^applicant/(?P<user>\w+)/$',applicantviews.applicant_view,name='applicant'),
    re_path(r'^applicant/(?P<user>\w+)/details',applicantviews.applicant_details_view,name='applicant_details'),
    path('accounts/google/login/',applicantviews.applicant_google_login_view,name='applicant_google_login'),
    path('applicant/role',applicantviews.set_applicant_user_role_view,name='set_applicant_user_role'),
    re_path(r'^applicant/(?P<user>\w+)/github/$',applicantviews.github_view,name='github'),
    re_path(r'^applicant/(?P<user>\w+)/codeforces/$',applicantviews.codeforces_view,name='codeforces'),
    re_path(r'^applicant/(?P<user>\w+)/codechef/$',applicantviews.codechef_view,name='codechef'),
    re_path(r'^applicant/(?P<user>\w+)/leetcode/$',applicantviews.leetcode_view,name='leetcode'),

    # url for company app
    path('company/accounts/login/',companyviews.company_login_view,name='company_login'),
    path('company/accounts/register/',companyviews.company_registration_view,name='company_register'),
    re_path(r'^company/(?P<user>\w+)/$',companyviews.company_view,name='company'),
    re_path(r'^company/(?P<user>\w+)/details',companyviews.company_details_view,name='company_details'),
    path('accounts/google/login',companyviews.company_google_login_view,name='company_google_login'),
    path('company/role',companyviews.set_company_user_role_view,name='set_company_user_role'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
