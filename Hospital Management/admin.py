

from django.contrib import admin
from .models import *
# Register models.


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name','mobile_no')


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('name','mobile_no','email','address')


@admin.register(Visits)
class VisitsAdmin(admin.ModelAdmin):
    list_display = ('visit_date','purpose_of_visit','height','weight','temperature','bp','notes')
