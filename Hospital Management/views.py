from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required,user_passes_test
from datetime import datetime,timedelta,date
from django.conf import settings


# Create home view
def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'app/homebase.html')


#for showing signup/login button for admin
def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'app/adminclick.html')


#for showing signup/login button for doctor
def doctorclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'app/doctorclick.html')

def admin_signup_view(request):
    form=forms.AdminSigupForm()
    if request.method=='POST':
        form=forms.AdminSigupForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.set_password(user.password)
            user.save()
            my_admin_group = Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(user)
            return HttpResponseRedirect('adminlogin')
    return render(request,'app/adminsignup.html',{'form':form})

def doctor_signup_view(request):
    userForm=forms.DoctorUserForm()
    doctorForm=forms.DoctorForm()
    mydict={'userForm':userForm,'doctorForm':doctorForm}
    if request.method=='POST':
        userForm=forms.DoctorUserForm(request.POST)
        doctorForm=forms.DoctorForm(request.POST,request.FILES)
        if userForm.is_valid() and doctorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            doctor=doctorForm.save(commit=False)
            doctor.user=user
            doctor=doctor.save()
            my_doctor_group = Group.objects.get_or_create(name='DOCTOR')
            my_doctor_group[0].user_set.add(user)
        return HttpResponseRedirect('doctorlogin')
    return render(request,'app/doctorsignup.html',context=mydict)

def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()
def is_doctor(user):
    return user.groups.filter(name='DOCTOR').exists()

def afterlogin_view(request):
    if is_admin(request.user):
        return redirect('admin-dashboard')
    elif is_doctor(request.user):
        accountapproval=models.Doctor.objects.all().filter(user_id=request.user.id)
        if accountapproval:
            return redirect('doctor-dashboard')
        else:
            return render(request,'app/doctor_wait_for_approval.html')
    
##Admin dashboard##
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_dashboard_view(request):
    
    doctors=models.Doctor.objects.all().order_by('-id')
    patients=models.Patient_details.objects.all().order_by('-id')
  
    doctorcount=models.Doctor.objects.all().count()
    pendingdoctorcount=models.Doctor.objects.all().count()

    patientcount=models.Patient_details.objects.all().count()
    pendingpatientcount=models.Patient_details.objects.all().count()

    mydict={
    'doctors':doctors,
    'patients':patients,
    'doctorcount':doctorcount,
    'pendingdoctorcount':pendingdoctorcount,
    'patientcount':patientcount,
    'pendingpatientcount':pendingpatientcount,
   
    }
    return render(request,'app/admin_dashboard.html',context=mydict)

##CRUD operation by admin##
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_doctor_view(request):
    return render(request,'app/admin_doctor.html')


##doctor view##
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_doctor_view(request):
    doctors=models.Doctor.objects.all()
    return render(request,'app/admin_view_doctor.html',{'doctors':doctors})


##delete doctor by admin##
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_doctor_from_hospital_view(request,pk):
    doctor=models.Doctor.objects.get(id=pk)
    user=models.User.objects.get(id=doctor.user_id)
    user.delete()
    doctor.delete()
    return redirect('admin-view-doctor')


##Update doctor by admin##
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_doctor_view(request,pk):
    doctor=models.Doctor.objects.get(id=pk)
    user=models.User.objects.get(id=doctor.user_id)

    userForm=forms.DoctorUserForm(instance=user)
    doctorForm=forms.DoctorForm(request.FILES,instance=doctor)
    mydict={'userForm':userForm,'doctorForm':doctorForm}
    if request.method=='POST':
        userForm=forms.DoctorUserForm(request.POST,instance=user)
        doctorForm=forms.DoctorForm(request.POST,request.FILES,instance=doctor)
        if userForm.is_valid() and doctorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            doctor=doctorForm.save(commit=False)
            doctor.status=True
            doctor.save()
            return redirect('admin-view-doctor')
    return render(request,'app/admin_update_doctor.html',context=mydict)



##Create new doctor by admin##
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_doctor_view(request):
    userForm=forms.DoctorUserForm()
    doctorForm=forms.DoctorForm()
    mydict={'userForm':userForm,'doctorForm':doctorForm}
    if request.method=='POST':
        userForm=forms.DoctorUserForm(request.POST)
        doctorForm=forms.DoctorForm(request.POST, request.FILES)
        if userForm.is_valid() and doctorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()

            doctor=doctorForm.save(commit=False)
            doctor.user=user
            doctor.status=True
            doctor.save()

            my_doctor_group = Group.objects.get_or_create(name='DOCTOR')
            my_doctor_group[0].user_set.add(user)

        return HttpResponseRedirect('admin-view-doctor')
    return render(request,'app/admin_add_doctor.html',context=mydict) 

##Admin patient view##   
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_patient_view(request):
    return render(request,'app/admin_patient.html')


##patient view##   
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_patient_view(request):
    patients=models.Patient_details.objects.all()
    return render(request,'app/admin_view_patient.html',{'patients':patients})


##delete patient by admin##   
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_patient_from_hospital_view(request,pk):
    patient=models.Patient_details.objects.get(id=pk)
    user=models.User.objects.get(id=patient.user_id)
    user.delete()
    patient.delete()
    return redirect('admin-view-patient')


##update patient by admin##   
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_patient_view(request,pk):
    patient=models.Patient_details.objects.get(id=pk)
    user=models.User.objects.get(id=patient.user_id)
    userForm=forms.PatientUserForm(instance=user)
    patientForm=forms.PatientForm(request.FILES,instance=patient)
    mydict={'userForm':userForm,'patientForm':patientForm}
    if request.method=='POST':
        userForm=forms.PatientUserForm(request.POST,instance=user)
        patientForm=forms.PatientForm(request.POST,request.FILES,instance=patient)
        if userForm.is_valid() and patientForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            patient=patientForm.save(commit=False)
            patient.status=True
            patient.assignedDoctorId=request.POST.get('assignedDoctorId')
            patient.save()
            return redirect('admin-view-patient')
    return render(request,'app/admin_update_patient.html',context=mydict)



##create new patient by admin##   
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_patient_view(request):
    userForm=forms.PatientUserForm()
    patientForm=forms.PatientForm()
    mydict={'userForm':userForm,'patientForm':patientForm}
    if request.method=='POST':
        userForm=forms.PatientUserForm(request.POST)
        patientForm=forms.PatientForm(request.POST,request.FILES)
        if userForm.is_valid() and patientForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()

            patient=patientForm.save(commit=False)
            patient.user=user
            patient.status=True
            patient.assignedDoctorId=request.POST.get('assignedDoctorId')
            patient.save()

            my_patient_group = Group.objects.get_or_create(name='PATIENT')
            my_patient_group[0].user_set.add(user)

        return HttpResponseRedirect('admin-view-patient')
    return render(request,'app/admin_add_patient.html',context=mydict)

##Doctor dashboard##
@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_dashboard_view(request):
    patientcount=models.Patient_details.objects.all().filter(assignedDoctorId=request.user.id).count()
    visits=models.Visits_Details.objects.all().filter(doctorId=request.user.id).order_by('-id')
    patientid=[]
    for a in visits:
        patientid.append(a.patientId)
    patients=models.Patient_details.objects.all().filter(user_id__in=patientid).order_by('-id')
    visits=zip(visits,patients)
    mydict={
    'patientcount':patientcount,
    'visits':visits,
    'doctor':models.Doctor.objects.get(user_id=request.user.id),
    }
    return render(request,'app/doctor_dashboard.html',context=mydict)


@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_patient_view(request):
    mydict={
    'doctor':models.Doctor.objects.get(user_id=request.user.id)
    }
    return render(request,'app/doctor_patient.html',context=mydict)


@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_view_patient_view(request):
    patients=models.Patient_details.objects.all().filter(assignedDoctorId=request.user.id)
    doctor=models.Doctor.objects.get(user_id=request.user.id)
    return render(request,'app/doctor_view_patient.html',{'patients':patients,'doctor':doctor})
