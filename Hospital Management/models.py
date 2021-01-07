"""
Definition of models.
"""
from django.db import models
from django.contrib.auth.models import User

class Doctor(models.Model):
    user = models.OneToOneField(User,null = True,on_delete=models.CASCADE)
    name=models.CharField(max_length=200,null=True)
    mobile_no= models.CharField(max_length=200,null=True)

    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return "({})".format(self.user.first_name)

class Patient_details(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=200,null=True)
    mobile_no= models.CharField(max_length=200,null=True)
    email= models.CharField(max_length=200,null=True)
    address= models.CharField(max_length=200,null=True)
    assignedDoctorId = models.PositiveIntegerField(null=True)

    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return self.user.first_name


class Visits_Details(models.Model):
    patientId=models.PositiveIntegerField(null=True)
    doctorId=models.PositiveIntegerField(null=True)
    patientName=models.CharField(max_length=40,null=True)
    doctorName=models.CharField(max_length=40,null=True)
    visit_date = models.DateField(null=True)
    purpose_of_visit = models.CharField(max_length=200,null=True)
    height = models.IntegerField(null=True)
    weight = models.IntegerField(null=True)
    temperature = models.IntegerField(null=True)
    bp = models.IntegerField(null=True)
    notes =  models.CharField(max_length=200,null=True)

    

    


    

    
