"""drowsiness URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('',views.index,name="index"),
    path('index',views.index,name="index"),
    path('AdminHome',views.AdminHome,name="AdminHome"),
    path('UserHome',views.UserHome,name="UserHome"),
    path('StaffHome',views.StaffHome,name="StaffHome"),
    # path('accounts/Login/',auth_views.LoginView.as_view(template_name='index.html'), name='Login'),
    # path('Logout', LogoutView.as_view(), name='Logout'),
    path('Login',views.Login,name="Login"),
    path('Privacy',views.Privacy,name="Privacy"),
    path('Logout',views.Logout,name="Logout"),
    path('Appoint_Staff',views.Appoint_Staff,name="Appoint_Staff"),
    path('Our_Staff',views.Our_Staff,name="Our_Staff"),
    path('delete_staff',views.delete_staff,name="delete_staff"),
    path('Our_Users',views.Our_Users,name="Our_Users"),
    path('Current_Users',views.Current_Users,name="Current_Users"),
    path('delete_user',views.delete_user,name="delete_user"),
    path('delete_user1',views.delete_user1,name="delete_user1"),
    path('Register_vehicle',views.Register_vehicle,name="Register_vehicle"),
    path('Manage_complaints',views.Manage_complaints,name="Manage_complaints"),
    path('my_reports',views.my_reports,name="my_reports"),
    path('my_Payemnts',views.my_Payemnts,name="my_Payemnts"),
    path('complaints',views.complaints,name="complaints"),
    path('fine_pay',views.fine_pay,name="fine_pay"),
    path('reports',views.reports,name="reports"),
    path('fine_report',views.fine_report,name="fine_report"),
    path('alert',views.alert,name="alert"),
    path('pays',views.pays,name="pays"),
    path('detect_sleep',views.detect_sleep,name="detect_sleep"),
    path("scrsht",views.scrsht,name="scrsht"),
    path("screensht",views.screensht,name="screensht"),
    path("add_fine",views.add_fine,name="add_fine"),
    path("payment_request",views.payment_request,name="payment_request"),
    path("admin_payment",views.admin_payment,name="admin_payment"),
    path("adminscreensht",views.adminscreensht,name="adminscreensht"),

    
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
