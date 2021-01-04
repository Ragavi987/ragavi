"""
Definition of urls for hospital_management.
"""

from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views
from django.urls import path

urlpatterns = [
    path('', views.home_view, name='home'),
    path('adminclick_view/', views.adminclick_view, name='adminclick_view'),
    path('doctorclick_view/', views.doctorclick_view, name='doctorclick_view'),
    path('admin_signup_view/', views.admin_signup_view, name='admin_signup_view'),
    path('doctor_signup_view/', views.doctor_signup_view, name='doctor_signup_view'),
    path('adminlogin', views.admin_signup_view, name='adminlogin'),
    path('doctorlogin',views.doctor_signup_view, name='doctorlogin'),
    path('afterlogin/', views.afterlogin_view,name='afterlogin'),
    path('admin-dashboard', views.admin_dashboard_view,name='admin-dashboard'),
    path('logout', LogoutView.as_view(template_name='app/home_view.html'),name='logout'),
    path('admin-doctor/', views.admin_doctor_view,name='admin-doctor'),
    path('admin-view-doctor/', views.admin_view_doctor_view,name='admin-view-doctor'),
    path('delete-doctor-from-hospital/<int:pk>', views.delete_doctor_from_hospital_view,name='delete-doctor-from-hospital'),
    path('update-doctor/<int:pk>', views.update_doctor_view,name='update-doctor'),
    path('admin-add-doctor/', views.admin_add_doctor_view,name='admin-add-doctor'),

    path('admin-patient/', views.admin_patient_view,name='admin-patient'),
    path('admin-view-patient/', views.admin_view_patient_view,name='admin-view-patient'),
    path('delete-patient-from-hospital/<int:pk>', views.delete_patient_from_hospital_view,name='delete-patient-from-hospital'),
    path('update-patient/<int:pk>', views.update_patient_view,name='update-patient'),
    path('admin-add-patient/', views.admin_add_patient_view,name='admin-add-patient'),
    path('doctor-dashboard/', views.doctor_dashboard_view,name='doctor-dashboard'),
    path('doctor-patient/', views.doctor_patient_view,name='doctor-patient'),
    path('doctor-view-patient/', views.doctor_view_patient_view,name='doctor-view-patient'),
    path('admin/', admin.site.urls)
]
